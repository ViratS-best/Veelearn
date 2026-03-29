import { useEffect, useRef, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useAuth, API_BASE_URL } from '@/context/AuthContext'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { toast } from 'sonner'
import { ArrowLeft, Play, Pause, RotateCcw, Settings, Download, Star } from 'lucide-react'

interface Simulator {
  id: number
  name: string
  description: string
  category: string
  content: string
}

export default function SimulatorViewPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { token } = useAuth()
  const iframeRef = useRef<HTMLIFrameElement>(null)
  const [simulator, setSimulator] = useState<Simulator | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isRunning, setIsRunning] = useState(false)

  useEffect(() => {
    if (id && token) {
      loadSimulator()
    }
  }, [id, token])

  const loadSimulator = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/simulators/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      const data = await response.json()
      
      if (data.success) {
        setSimulator(data.data)
      } else {
        toast.error('Simulator not found')
        navigate('/marketplace')
      }
    } catch (error) {
      toast.error('Failed to load simulator')
    } finally {
      setIsLoading(false)
    }
  }

  const getSimulatorUrl = () => {
    const path = window.location.pathname
    if (path.includes('github.io')) {
      return 'https://virat-sisodiya.github.io/Veelearn/veelearn-frontend/simulator-view.html'
    }
    return '/simulator-view.html'
  }

  const handleRun = () => {
    if (iframeRef.current?.contentWindow) {
      iframeRef.current.contentWindow.postMessage({ type: 'run' }, '*')
      setIsRunning(true)
    }
  }

  const handleStop = () => {
    if (iframeRef.current?.contentWindow) {
      iframeRef.current.contentWindow.postMessage({ type: 'stop' }, '*')
      setIsRunning(false)
    }
  }

  const handleReset = () => {
    if (iframeRef.current?.contentWindow) {
      iframeRef.current.contentWindow.postMessage({ type: 'reset' }, '*')
      setIsRunning(false)
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-muted-foreground">Loading simulator...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <header className="border-b border-border bg-surface">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button variant="ghost" size="icon" onClick={() => navigate(-1)}>
                <ArrowLeft className="h-5 w-5" />
              </Button>
              <div>
                <h1 className="font-heading font-semibold">{simulator?.name}</h1>
                <p className="text-sm text-muted-foreground">{simulator?.description}</p>
              </div>
            </div>
            <div className="flex gap-2">
              {!isRunning ? (
                <Button onClick={handleRun}>
                  <Play className="h-4 w-4 mr-2" />
                  Run
                </Button>
              ) : (
                <Button onClick={handleStop}>
                  <Pause className="h-4 w-4 mr-2" />
                  Stop
                </Button>
              )}
              <Button variant="outline" onClick={handleReset}>
                <RotateCcw className="h-4 w-4 mr-2" />
                Reset
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
          sandbox="allow-scripts allow-same-origin"
          title="Simulator Viewer"
        />
      </div>
    </div>
  )
}
