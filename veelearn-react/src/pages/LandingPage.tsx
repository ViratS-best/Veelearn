import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '@/context/AuthContext'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Loader2 } from 'lucide-react'

export default function LandingPage() {
  const navigate = useNavigate()
  const { token } = useAuth()
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (token) {
      navigate('/dashboard')
    } else {
      setIsLoading(false)
    }
  }, [token, navigate])

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Aurora Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="aurora-1" />
        <div className="aurora-2" />
        <div className="aurora-3" />
      </div>

      {/* Header */}
      <header className="relative z-10 border-b border-border/50 bg-background/80 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-3xl font-heading font-bold text-highlight">Veelearn</h1>
            <div className="flex gap-2">
              <Button variant="ghost" onClick={() => navigate('/login')}>Login</Button>
              <Button onClick={() => navigate('/login')}>Get Started</Button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="relative z-10 container mx-auto px-4 py-24">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-5xl md:text-7xl font-heading font-bold mb-6 bg-gradient-to-r from-highlight via-vee-aqua to-primary bg-clip-text text-transparent">
            Learn Interactively
          </h2>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Create and explore interactive courses with block-based simulators, 
            visual programming, and AI-powered learning experiences.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" onClick={() => navigate('/login')}>
              Start Learning Free
            </Button>
            <Button size="lg" variant="outline" onClick={() => navigate('/login')}>
              Create a Course
            </Button>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-24">
          <Card className="bg-surface/50 backdrop-blur">
            <CardContent className="p-6">
              <div className="h-12 w-12 rounded-lg bg-highlight/20 flex items-center justify-center mb-4">
                <svg className="h-6 w-6 text-highlight" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" />
                </svg>
              </div>
              <h3 className="text-xl font-heading font-semibold mb-2">Block Simulators</h3>
              <p className="text-muted-foreground">
                Create interactive physics simulations using our intuitive block-based editor. No coding required.
              </p>
            </CardContent>
          </Card>

          <Card className="bg-surface/50 backdrop-blur">
            <CardContent className="p-6">
              <div className="h-12 w-12 rounded-lg bg-vee-purple/20 flex items-center justify-center mb-4">
                <svg className="h-6 w-6 text-vee-purple" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <h3 className="text-xl font-heading font-semibold mb-2">Visual Programming</h3>
              <p className="text-muted-foreground">
                Build code-based visual simulations with our powerful editor. Bring your ideas to life visually.
              </p>
            </CardContent>
          </Card>

          <Card className="bg-surface/50 backdrop-blur">
            <CardContent className="p-6">
              <div className="h-12 w-12 rounded-lg bg-vee-aqua/20 flex items-center justify-center mb-4">
                <svg className="h-6 w-6 text-vee-aqua" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <h3 className="text-xl font-heading font-semibold mb-2">Course Creation</h3>
              <p className="text-muted-foreground">
                Design engaging courses with text, images, LaTeX equations, quizzes, and interactive simulators.
              </p>
            </CardContent>
          </Card>
        </div>

        {/* CTA */}
        <div className="text-center mt-24">
          <h3 className="text-2xl font-heading font-bold mb-4">Ready to get started?</h3>
          <Button size="lg" onClick={() => navigate('/login')}>
            Join Veelearn Today
          </Button>
        </div>
      </main>

      {/* Footer */}
      <footer className="relative z-10 border-t border-border mt-24">
        <div className="container mx-auto px-4 py-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div>
              <h4 className="font-heading font-bold text-highlight">Veelearn</h4>
              <p className="text-sm text-muted-foreground">Interactive learning platform</p>
            </div>
            <p className="text-sm text-muted-foreground">
              © 2026 Veelearn. All rights reserved.
            </p>
          </div>
        </div>
      </footer>

      <style>{`
        .aurora-1 {
          position: absolute;
          top: -50%;
          left: -50%;
          width: 200%;
          height: 200%;
          background: radial-gradient(circle at 30% 30%, rgba(34, 197, 94, 0.15) 0%, transparent 50%);
          animation: aurora 20s ease-in-out infinite;
        }
        .aurora-2 {
          position: absolute;
          top: -50%;
          left: -50%;
          width: 200%;
          height: 200%;
          background: radial-gradient(circle at 70% 60%, rgba(59, 130, 246, 0.1) 0%, transparent 40%);
          animation: aurora 25s ease-in-out infinite reverse;
        }
        .aurora-3 {
          position: absolute;
          top: -30%;
          left: -30%;
          width: 160%;
          height: 160%;
          background: radial-gradient(circle at 50% 80%, rgba(139, 92, 246, 0.08) 0%, transparent 35%);
          animation: aurora 30s ease-in-out infinite;
        }
        @keyframes aurora {
          0%, 100% { transform: translate(0, 0) rotate(0deg); }
          33% { transform: translate(5%, 5%) rotate(5deg); }
          66% { transform: translate(-5%, 3%) rotate(-3deg); }
        }
      `}</style>
    </div>
  )
}
