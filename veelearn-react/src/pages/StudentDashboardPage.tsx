import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth, API_BASE_URL } from '@/context/AuthContext'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardFooter, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { toast } from 'sonner'
import {
  ArrowLeft,
  Users,
  BookOpen,
  Plus,
  Play,
  Clock,
  CheckCircle,
  AlertCircle
} from 'lucide-react'

interface Assignment {
  id: number
  course_id: number
  course_title: string
  teacher_name: string
  due_date?: string
  progress?: number
  status?: string
}

export default function StudentDashboardPage() {
  const navigate = useNavigate()
  const { token } = useAuth()
  const [assignments, setAssignments] = useState<Assignment[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [showJoinDialog, setShowJoinDialog] = useState(false)
  const [classCode, setClassCode] = useState('')
  const [enrolledCourses, setEnrolledCourses] = useState<any[]>([])

  useEffect(() => {
    if (token) {
      loadStudentData()
    }
  }, [token])

  const loadStudentData = async () => {
    try {
      const headers = { Authorization: `Bearer ${token}` }
      
      // Load assignments
      const assignmentsRes = await fetch(`${API_BASE_URL}/api/student/assignments`, { headers })
      const assignmentsData = await assignmentsRes.json()
      if (assignmentsData.success) {
        setAssignments(assignmentsData.data || [])
      }

      // Load enrolled courses
      const enrolledRes = await fetch(`${API_BASE_URL}/api/users/enrollments`, { headers })
      const enrolledData = await enrolledRes.json()
      if (enrolledData.success) {
        setEnrolledCourses(enrolledData.data || [])
      }
    } catch (error) {
      console.error('Failed to load student data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const joinClass = async () => {
    if (!classCode.trim()) {
      toast.error('Please enter a class code')
      return
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/student/enroll-class`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ class_code: classCode }),
      })

      const data = await response.json()
      if (data.success) {
        toast.success('Joined class successfully!')
        setShowJoinDialog(false)
        loadStudentData()
      } else {
        toast.error(data.message || 'Failed to join class')
      }
    } catch (error) {
      toast.error('Failed to join class')
    }
  }

  const submitProgress = async (courseId: number, progress: number) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/student/submit-assignment`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ course_id: courseId, progress }),
      })

      const data = await response.json()
      if (data.success) {
        toast.success('Progress submitted!')
        loadStudentData()
      } else {
        toast.error(data.message || 'Failed to submit')
      }
    } catch (error) {
      toast.error('Failed to submit progress')
    }
  }

  const getStatusBadge = (assignment: Assignment) => {
    const isOverdue = assignment.due_date && new Date(assignment.due_date) < new Date()
    const isComplete = assignment.progress === 100

    if (isComplete) {
      return <span className="flex items-center gap-1 text-green-400 text-sm"><CheckCircle className="h-4 w-4" /> Completed</span>
    }
    if (isOverdue) {
      return <span className="flex items-center gap-1 text-red-400 text-sm"><AlertCircle className="h-4 w-4" /> Overdue</span>
    }
    return <span className="flex items-center gap-1 text-yellow-400 text-sm"><Clock className="h-4 w-4" /> In Progress</span>
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-muted-foreground">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border bg-surface">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button variant="ghost" size="icon" onClick={() => navigate('/dashboard')}>
                <ArrowLeft className="h-5 w-5" />
              </Button>
              <Users className="h-8 w-8 text-primary" />
              <div>
                <h1 className="text-2xl font-heading font-bold">Student Dashboard</h1>
                <p className="text-muted-foreground">Your enrolled courses and assignments</p>
              </div>
            </div>
            <Button onClick={() => setShowJoinDialog(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Join a Class
            </Button>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <Tabs defaultValue="assignments" className="space-y-6">
          <TabsList>
            <TabsTrigger value="assignments">Assignments ({assignments.length})</TabsTrigger>
            <TabsTrigger value="courses">Enrolled Courses ({enrolledCourses.length})</TabsTrigger>
          </TabsList>

          <TabsContent value="assignments" className="space-y-4">
            {assignments.length === 0 ? (
              <div className="text-center py-12">
                <BookOpen className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p className="text-muted-foreground mb-4">No assignments yet</p>
                <Button onClick={() => setShowJoinDialog(true)}>
                  Join a Class
                </Button>
              </div>
            ) : (
              assignments.map((assignment) => (
                <Card key={assignment.id}>
                  <CardContent className="p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div>
                        <h3 className="font-semibold text-lg">{assignment.course_title}</h3>
                        <p className="text-sm text-muted-foreground">
                          Teacher: {assignment.teacher_name}
                        </p>
                      </div>
                      {getStatusBadge(assignment)}
                    </div>
                    
                    {assignment.due_date && (
                      <p className="text-sm text-muted-foreground mb-4">
                        Due: {new Date(assignment.due_date).toLocaleDateString()}
                      </p>
                    )}

                    <div className="space-y-2 mb-4">
                      <div className="flex justify-between text-sm">
                        <span>Progress</span>
                        <span>{assignment.progress || 0}%</span>
                      </div>
                      <Progress value={assignment.progress || 0} />
                    </div>

                    <div className="flex gap-2">
                      <Button onClick={() => navigate(`/courses/${assignment.course_id}`)}>
                        <Play className="h-4 w-4 mr-2" />
                        Continue Learning
                      </Button>
                      <Button variant="outline" onClick={() => submitProgress(assignment.course_id, 100)}>
                        Mark Complete
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </TabsContent>

          <TabsContent value="courses" className="space-y-4">
            {enrolledCourses.length === 0 ? (
              <div className="text-center py-12">
                <BookOpen className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p className="text-muted-foreground">Not enrolled in any courses</p>
              </div>
            ) : (
              enrolledCourses.map((enrollment) => (
                <Card key={enrollment.course_id}>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="font-semibold">{enrollment.course_title}</h3>
                        <p className="text-sm text-muted-foreground">
                          {enrollment.progress || 0}% complete
                        </p>
                      </div>
                      <Button onClick={() => navigate(`/courses/${enrollment.course_id}`)}>
                        <Play className="h-4 w-4 mr-2" />
                        Continue
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </TabsContent>
        </Tabs>
      </main>

      {/* Join Class Dialog */}
      {showJoinDialog && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <Card className="w-full max-w-md mx-4">
            <CardHeader>
              <CardTitle>Join a Class</CardTitle>
              <CardDescription>Enter your teacher's class code to join</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label>Class Code</Label>
                  <Input
                    value={classCode}
                    onChange={(e) => setClassCode(e.target.value)}
                    placeholder="e.g., ABC123"
                  />
                </div>
              </div>
            </CardContent>
            <CardFooter className="justify-end gap-2">
              <Button variant="outline" onClick={() => setShowJoinDialog(false)}>Cancel</Button>
              <Button onClick={joinClass}>Join Class</Button>
            </CardFooter>
          </Card>
        </div>
      )}
    </div>
  )
}
