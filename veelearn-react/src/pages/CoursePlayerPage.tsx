import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useAuth, API_BASE_URL } from '@/context/AuthContext'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { toast } from 'sonner'
import {
  ArrowLeft,
  ArrowRight,
  ChevronLeft,
  ChevronRight,
  Menu,
  X,
  CheckCircle,
  Play,
  Blocks,
  Code
} from 'lucide-react'

interface Course {
  id: number
  title: string
  description: string
  content: string
  course_type: string
}

interface Unit {
  id: number
  title: string
  order_index: number
  content?: string
}

interface Progress {
  completed_units: number
  total_units: number
}

export default function CoursePlayerPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { token } = useAuth()
  const [course, setCourse] = useState<Course | null>(null)
  const [units, setUnits] = useState<Unit[]>([])
  const [currentUnitIndex, setCurrentUnitIndex] = useState(0)
  const [progress, setProgress] = useState<Progress>({ completed_units: 0, total_units: 0 })
  const [showSidebar, setShowSidebar] = useState(true)
  const [isLoading, setIsLoading] = useState(true)
  const [isBattlePlaying, setIsBattlePlaying] = useState(false)

  useEffect(() => {
    // Load anime-battle-system.js
    const script = document.createElement('script')
    script.src = `${import.meta.env.BASE_URL.replace(/\/$/, '')}/vanilla/anime-battle-system.js`
    script.async = true
    document.body.appendChild(script)

    if (id && token) {
      loadCourse()
    }
  }, [id, token])

  const loadCourse = async () => {
    try {
      const [courseRes, progressRes] = await Promise.all([
        fetch(`${API_BASE_URL}/api/courses/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        }),
        fetch(`${API_BASE_URL}/api/student/course/${id}/progress`, {
          headers: { Authorization: `Bearer ${token}` },
        })
      ])

      const courseData = await courseRes.json()
      const progressData = await progressRes.json()

      if (courseData.success) {
        setCourse(courseData.data)
        
        // Load units
        if (courseData.data.course_type === 'master') {
          const unitsRes = await fetch(`${API_BASE_URL}/api/courses/${id}/units`, {
            headers: { Authorization: `Bearer ${token}` },
          })
          const unitsData = await unitsRes.json()
          if (unitsData.success) {
            setUnits(unitsData.data || [])
          }
        }
      }

      if (progressData.success) {
        setProgress(progressData.data || { completed_units: 0, total_units: 1 })
      }
    } catch (error) {
      toast.error('Failed to load course')
    } finally {
      setIsLoading(false)
    }
  }

  const markUnitComplete = async () => {
    const unit = units[currentUnitIndex]
    if (!unit) return

    try {
      await fetch(`${API_BASE_URL}/api/student/course/${id}/unit/${unit.id}/complete`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
      })
      
      setProgress(prev => ({
        ...prev,
        completed_units: prev.completed_units + 1
      }))

      if (currentUnitIndex < units.length - 1) {
        // Trigger Anime Battle before moving!
        setIsBattlePlaying(true)
        if ((window as any).createAnimeStyleBattle) {
          (window as any).createAnimeStyleBattle(() => {
            setIsBattlePlaying(false)
            setCurrentUnitIndex(prev => prev + 1)
          })
        } else {
          setCurrentUnitIndex(prev => prev + 1)
        }
      } else {
        toast.success('Congratulations! You completed the course!')
        setIsBattlePlaying(true)
        if ((window as any).createAnimeStyleBattle) {
          (window as any).createAnimeStyleBattle(() => {
            setIsBattlePlaying(false)
          })
        }
      }
    } catch (error) {
      console.error('Failed to mark unit complete:', error)
    }
  }

  const goToNext = () => {
    if (currentUnitIndex < units.length - 1) {
      setCurrentUnitIndex(prev => prev + 1)
    }
  }

  const goToPrev = () => {
    if (currentUnitIndex > 0) {
      setCurrentUnitIndex(prev => prev - 1)
    }
  }

  const progressPercent = units.length > 0 
    ? Math.round((progress.completed_units / units.length) * 100)
    : 0

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-muted-foreground">Loading course...</div>
      </div>
    )
  }

  const currentUnit = units[currentUnitIndex]
  const hasUnits = units.length > 0

  return (
    <div className="min-h-screen bg-background flex">
      {/* Anime Battle Overlay */}
      {isBattlePlaying && (
         <div id="battle-container" className="fixed inset-0 z-[9999] bg-black"></div>
      )}

      {/* Sidebar */}
      <aside 
        className={`${showSidebar ? 'w-72' : 'w-0'} fixed inset-y-0 left-0 z-40 bg-surface border-r border-border transition-all duration-300 overflow-hidden`}
      >
        <div className="w-72 h-full flex flex-col">
          {/* Header */}
          <div className="p-4 border-b border-border">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-heading font-semibold truncate">{course?.title}</h2>
              <Button variant="ghost" size="icon" onClick={() => setShowSidebar(false)}>
                <X className="h-4 w-4" />
              </Button>
            </div>
            
            {/* Progress */}
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Progress</span>
                <span>{progressPercent}%</span>
              </div>
              <Progress value={progressPercent} className="h-2" />
              <p className="text-xs text-muted-foreground">
                {progress.completed_units} of {units.length} completed
              </p>
            </div>
          </div>

          {/* Units List */}
          <div className="flex-1 overflow-y-auto p-2">
            {hasUnits ? (
              <div className="space-y-1">
                {units.map((unit, index) => (
                  <button
                    key={unit.id}
                    onClick={() => setCurrentUnitIndex(index)}
                    className={`w-full flex items-center gap-3 p-3 rounded-lg text-left transition-colors ${
                      index === currentUnitIndex
                        ? 'bg-primary/20 text-primary'
                        : 'hover:bg-muted'
                    }`}
                  >
                    <div className={`h-6 w-6 rounded-full flex items-center justify-center text-xs ${
                      index < progress.completed_units
                        ? 'bg-green-600 text-white'
                        : index === currentUnitIndex
                        ? 'bg-primary text-white'
                        : 'bg-muted text-muted-foreground'
                    }`}>
                      {index < progress.completed_units ? (
                        <CheckCircle className="h-4 w-4" />
                      ) : (
                        index + 1
                      )}
                    </div>
                    <span className="text-sm truncate">{unit.title}</span>
                  </button>
                ))}
              </div>
            ) : (
              <p className="text-center text-muted-foreground py-8">
                No units available
              </p>
            )}
          </div>

          {/* Back to Dashboard */}
          <div className="p-4 border-t border-border">
            <Button variant="outline" className="w-full" onClick={() => navigate('/dashboard')}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              Dashboard
            </Button>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className={`flex-1 transition-all duration-300 ${showSidebar ? 'ml-72' : 'ml-0'}`}>
        {/* Top Bar */}
        <header className="border-b border-border bg-surface sticky top-0 z-30">
          <div className="container mx-auto px-4 py-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                {!showSidebar && (
                  <Button variant="ghost" size="icon" onClick={() => setShowSidebar(true)}>
                    <Menu className="h-5 w-5" />
                  </Button>
                )}
                <h1 className="font-heading font-semibold">
                  {hasUnits ? currentUnit?.title : course?.title}
                </h1>
              </div>
              
              <div className="flex items-center gap-2">
                <Button variant="outline" size="sm" onClick={goToPrev} disabled={currentUnitIndex === 0}>
                  <ChevronLeft className="h-4 w-4" />
                </Button>
                <span className="text-sm text-muted-foreground">
                  {currentUnitIndex + 1} / {units.length || 1}
                </span>
                <Button variant="outline" size="sm" onClick={goToNext} disabled={currentUnitIndex === units.length - 1}>
                  <ChevronRight className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        </header>

        {/* Content Area */}
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-4xl mx-auto">
            <Card>
              <CardContent className="p-8">
                {hasUnits ? (
                  <div 
                    className="prose prose-invert max-w-none"
                    dangerouslySetInnerHTML={{ __html: currentUnit?.content || '<p>No content available</p>' }}
                  />
                ) : (
                  <div 
                    className="prose prose-invert max-w-none"
                    dangerouslySetInnerHTML={{ __html: course?.content || '<p>No content available</p>' }}
                  />
                )}

                {/* Interactive Elements Detection */}
                <div className="mt-8 pt-8 border-t border-border">
                  <p className="text-sm text-muted-foreground mb-4">
                    This content may include interactive elements:
                  </p>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm" onClick={() => window.open('/block-simulator', '_blank')}>
                      <Blocks className="h-4 w-4 mr-2" />
                      Block Simulator
                    </Button>
                    <Button variant="outline" size="sm" onClick={() => window.open('/visual-simulator', '_blank')}>
                      <Code className="h-4 w-4 mr-2" />
                      Visual Simulator
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Navigation Buttons */}
            <div className="flex justify-between mt-8">
              <Button 
                variant="outline" 
                onClick={goToPrev}
                disabled={currentUnitIndex === 0}
              >
                <ChevronLeft className="h-4 w-4 mr-2" />
                Previous
              </Button>
              
              <Button onClick={markUnitComplete}>
                {currentUnitIndex === units.length - 1 ? 'Complete Course' : 'Next Unit'}
                <ChevronRight className="h-4 w-4 ml-2" />
              </Button>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
