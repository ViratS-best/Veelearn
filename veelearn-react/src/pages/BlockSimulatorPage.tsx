import { useEffect, useRef, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth, API_BASE_URL } from '@/context/AuthContext'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { toast } from 'sonner'
import { ArrowLeft, Save, Play, Pause, RotateCcw, Trash2, Layers, Settings } from 'lucide-react'

interface Block {
  id: string
  type: string
  x: number
  y: number
  inputs: Record<string, any>
  connections: Record<string, { blockId: string; output: string }>
}

declare global {
  interface Window {
    blockTemplates: Record<string, any>
    createBlock: (type: string, x: number, y: number) => Block
    executeBlocks: (blocks: Block[], initialState: any) => Promise<any>
    runAnimation: () => void
    stopAnimation: () => void
  }
}

export default function BlockSimulatorPage() {
  const navigate = useNavigate()
  const { token, user } = useAuth()
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const workspaceRef = useRef<HTMLDivElement>(null)
  const [blocks, setBlocks] = useState<Block[]>([])
  const [selectedBlock, setSelectedBlock] = useState<string | null>(null)
  const [isRunning, setIsRunning] = useState(false)
  const [scriptsLoaded, setScriptsLoaded] = useState(false)
  const [showPublishDialog, setShowPublishDialog] = useState(false)
  const [simulatorName, setSimulatorName] = useState('')
  const [simulatorDescription, setSimulatorDescription] = useState('')
  const [isPublishing, setIsPublishing] = useState(false)
  const [blockTypes, setBlockTypes] = useState<string[]>([])

  // Load simulator scripts
  useEffect(() => {
    const loadScripts = async () => {
      const scripts = [
        '/simulators/block-templates-unified.js',
        '/simulators/block-physics-engine.js',
        '/simulators/block-renderer-system.js',
        '/simulators/block-animation.js',
        '/simulators/block-execution-engine.js'
      ]

      for (const src of scripts) {
        await new Promise<void>((resolve, reject) => {
          const script = document.createElement('script')
          script.src = src
          script.onload = () => resolve()
          script.onerror = () => reject(new Error(`Failed to load ${src}`))
          document.body.appendChild(script)
        })
      }

      // Get available block types
      if (window.blockTemplates) {
        setBlockTypes(Object.keys(window.blockTemplates))
      }
      
      setScriptsLoaded(true)
    }

    loadScripts().catch(err => {
      console.error('Failed to load scripts:', err)
      toast.error('Failed to load simulator')
    })
  }, [])

  // Initialize canvas
  useEffect(() => {
    if (!scriptsLoaded || !canvasRef.current) return
    
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // Set canvas size
    const resizeCanvas = () => {
      const rect = canvas.parentElement?.getBoundingClientRect()
      if (rect) {
        canvas.width = rect.width
        canvas.height = rect.height
      }
    }
    resizeCanvas()
    window.addEventListener('resize', resizeCanvas)

    // Animation loop
    let animationId: number
    const animate = () => {
      ctx.fillStyle = '#0a0a0a'
      ctx.fillRect(0, 0, canvas.width, canvas.height)
      
      // Draw blocks
      blocks.forEach(block => {
        const template = window.blockTemplates?.[block.type]
        if (!template) return

        ctx.fillStyle = template.color || '#3b82f6'
        ctx.fillRect(block.x, block.y, 120, 60)
        
        ctx.fillStyle = '#fff'
        ctx.font = '14px sans-serif'
        ctx.fillText(template.title || block.type, block.x + 10, block.y + 25)
      })

      // Draw selected block highlight
      if (selectedBlock) {
        const block = blocks.find(b => b.id === selectedBlock)
        if (block) {
          ctx.strokeStyle = '#22c55e'
          ctx.lineWidth = 3
          ctx.strokeRect(block.x - 3, block.y - 3, 126, 66)
        }
      }

      animationId = requestAnimationFrame(animate)
    }
    animate()

    return () => {
      cancelAnimationFrame(animationId)
      window.removeEventListener('resize', resizeCanvas)
    }
  }, [scriptsLoaded, blocks, selectedBlock])

  const addBlock = (type: string) => {
    if (!window.blockTemplates?.[type]) return
    
    const newBlock: Block = {
      id: `block_${Date.now()}`,
      type,
      x: 50 + Math.random() * 200,
      y: 50 + Math.random() * 200,
      inputs: {},
      connections: {}
    }
    setBlocks([...blocks, newBlock])
    setSelectedBlock(newBlock.id)
  }

  const deleteBlock = (blockId: string) => {
    setBlocks(blocks.filter(b => b.id !== blockId))
    if (selectedBlock === blockId) {
      setSelectedBlock(null)
    }
  }

  const runSimulation = async () => {
    if (!canvasRef.current || blocks.length === 0) return
    
    setIsRunning(true)
    
    try {
      // Execute blocks
      const result = await window.executeBlocks?.(blocks, {}) || {}
      console.log('Simulation result:', result)
      toast.success('Simulation completed!')
    } catch (error) {
      console.error('Simulation error:', error)
      toast.error('Simulation failed')
    } finally {
      setIsRunning(false)
    }
  }

  const stopSimulation = () => {
    window.stopAnimation?.()
    setIsRunning(false)
  }

  const clearCanvas = () => {
    setBlocks([])
    setSelectedBlock(null)
  }

  const publishSimulator = async () => {
    if (!simulatorName.trim()) {
      toast.error('Please enter a simulator name')
      return
    }

    setIsPublishing(true)
    try {
      const response = await fetch(`${API_BASE_URL}/api/simulators`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          name: simulatorName,
          description: simulatorDescription,
          category: 'block',
          is_public: true,
          content: JSON.stringify({ blocks, type: 'block' }),
        }),
      })

      const data = await response.json()

      if (data.success) {
        toast.success('Simulator published!')
        setShowPublishDialog(false)
        navigate('/marketplace')
      } else {
        toast.error(data.message || 'Failed to publish')
      }
    } catch (error) {
      toast.error('Failed to publish')
    } finally {
      setIsPublishing(false)
    }
  }

  if (!scriptsLoaded) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-muted-foreground">Loading simulator...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Header */}
      <header className="border-b border-border bg-surface">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button variant="ghost" size="icon" onClick={() => navigate('/dashboard')}>
                <ArrowLeft className="h-5 w-5" />
              </Button>
              <div>
                <h1 className="font-heading font-semibold">Block Simulator</h1>
                <p className="text-sm text-muted-foreground">
                  {blocks.length} blocks on canvas
                </p>
              </div>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" onClick={clearCanvas}>
                <Trash2 className="h-4 w-4 mr-2" />
                Clear
              </Button>
              {isRunning ? (
                <Button variant="outline" onClick={stopSimulation}>
                  <Pause className="h-4 w-4 mr-2" />
                  Stop
                </Button>
              ) : (
                <Button onClick={runSimulation} disabled={blocks.length === 0}>
                  <Play className="h-4 w-4 mr-2" />
                  Run
                </Button>
              )}
              <Button onClick={() => setShowPublishDialog(true)}>
                Publish
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="flex-1 flex">
        {/* Block Palette */}
        <aside className="w-64 border-r border-border bg-surface p-4 overflow-y-auto">
          <h3 className="font-semibold mb-3">Blocks</h3>
          <div className="space-y-1">
            {blockTypes.map(type => {
              const template = window.blockTemplates?.[type]
              return (
                <button
                  key={type}
                  onClick={() => addBlock(type)}
                  className="w-full text-left p-2 rounded-md bg-muted hover:bg-accent transition-colors text-sm"
                  style={{ borderLeft: `3px solid ${template?.color || '#3b82f6'}` }}
                >
                  {template?.title || type}
                </button>
              )
            })}
          </div>
        </aside>

        {/* Canvas */}
        <main className="flex-1 relative">
          <div ref={workspaceRef} className="absolute inset-0">
            <canvas ref={canvasRef} className="w-full h-full" />
          </div>
          
          {/* Tips */}
          <div className="absolute bottom-4 left-4 text-sm text-muted-foreground bg-background/80 p-2 rounded">
            Click a block to select • Delete key to remove
          </div>
        </main>
      </div>

      {/* Publish Dialog */}
      <Dialog open={showPublishDialog} onOpenChange={setShowPublishDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Publish Simulator</DialogTitle>
            <DialogDescription>Share your simulator with the Veelearn community</DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label>Simulator Name</Label>
              <Input
                value={simulatorName}
                onChange={(e) => setSimulatorName(e.target.value)}
                placeholder="My Awesome Simulator"
              />
            </div>
            <div className="space-y-2">
              <Label>Description</Label>
              <Input
                value={simulatorDescription}
                onChange={(e) => setSimulatorDescription(e.target.value)}
                placeholder="A brief description..."
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowPublishDialog(false)}>Cancel</Button>
            <Button onClick={publishSimulator} disabled={isPublishing}>
              {isPublishing ? 'Publishing...' : 'Publish'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
