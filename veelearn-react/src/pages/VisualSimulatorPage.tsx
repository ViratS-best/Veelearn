import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth, API_BASE_URL } from '@/context/AuthContext'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { toast } from 'sonner'
import { ArrowLeft, Save, ExternalLink } from 'lucide-react'

export default function VisualSimulatorPage() {
  const navigate = useNavigate()
  const { token } = useAuth()
  const iframeRef = useRef<HTMLIFrameElement>(null)
  const [showPublishDialog, setShowPublishDialog] = useState(false)
  const [simulatorName, setSimulatorName] = useState('')
  const [simulatorDescription, setSimulatorDescription] = useState('')
  const [isPublishing, setIsPublishing] = useState(false)

  const getSimulatorUrl = () => {
    const path = window.location.pathname
    if (path.includes('github.io')) {
      return 'https://virat-sisodiya.github.io/Veelearn/veelearn-frontend/visual-simulator.html'
    }
    return '/visual-simulator.html'
  }

  useEffect(() => {
    const handleMessage = async (event: MessageEvent) => {
      if (event.data.type === 'close') {
        navigate('/dashboard')
      }
    }

    window.addEventListener('message', handleMessage)
    return () => window.removeEventListener('message', handleMessage)
  }, [navigate])

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
          category: 'visual',
          is_public: true,
          content: JSON.stringify({ type: 'visual' }),
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

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <header className="border-b border-border bg-surface">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button variant="ghost" size="icon" onClick={() => navigate('/dashboard')}>
                <ArrowLeft className="h-5 w-5" />
              </Button>
              <div>
                <h1 className="font-heading font-semibold">Visual Simulator</h1>
                <p className="text-sm text-muted-foreground">Create code-based visual simulations</p>
              </div>
            </div>
            <div className="flex gap-2">
              <Button onClick={() => setShowPublishDialog(true)}>
                <ExternalLink className="h-4 w-4 mr-2" />
                Publish
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="flex-1">
        <iframe
          ref={iframeRef}
          src={getSimulatorUrl()}
          className="w-full h-full border-0"
          sandbox="allow-scripts allow-same-origin allow-forms"
          title="Visual Simulator"
        />
      </div>

      <Dialog open={showPublishDialog} onOpenChange={setShowPublishDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Publish Simulator</DialogTitle>
            <DialogDescription>Share your simulator with the community</DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label>Name</Label>
              <Input value={simulatorName} onChange={(e) => setSimulatorName(e.target.value)} placeholder="My Simulator" />
            </div>
            <div className="space-y-2">
              <Label>Description</Label>
              <Input value={simulatorDescription} onChange={(e) => setSimulatorDescription(e.target.value)} placeholder="Description..." />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowPublishDialog(false)}>Cancel</Button>
            <Button onClick={publishSimulator} disabled={isPublishing}>Publish</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
