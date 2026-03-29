import { useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import { Button } from '@/components/ui/button'

export default function BlockSimulatorPage() {
  const navigate = useNavigate()
  const iframeRef = useRef<HTMLIFrameElement>(null)

  // Use Vite's BASE_URL to correctly resolve the path whether in dev or on GitHub Pages
  const basePath = import.meta.env.BASE_URL.replace(/\/$/, '')
  const simulatorUrl = `${basePath}/vanilla/block-simulator.html`

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Header */}
      <header className="border-b border-border bg-surface relative z-10">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon" onClick={() => navigate(-1)}>
              <ArrowLeft className="h-5 w-5" />
            </Button>
            <div>
              <h1 className="font-heading font-semibold text-lg text-foreground">Block Simulator Editor</h1>
              <p className="text-sm text-muted-foreground">
                Powered by Veelearn Canvas Engine
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Simulator Frame */}
      <div className="flex-1 w-full bg-black">
        <iframe 
          ref={iframeRef}
          src={simulatorUrl}
          className="w-full h-full border-none"
          title="Block Simulator Engine"
          allowFullScreen
        />
      </div>
    </div>
  )
}
