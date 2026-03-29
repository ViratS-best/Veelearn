import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth, API_BASE_URL } from '@/context/AuthContext'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { toast } from 'sonner'
import {
  ArrowLeft,
  GraduationCap,
  Users,
  BookOpen,
  Plus,
  Copy,
  Check,
  Eye,
  Clock,
  Settings
} from 'lucide-react'

interface Class {
  id: number
  class_code: string
  name?: string
  student_count?: number
}

interface Assignment {
  id: number
  course_title: string
  due_date?: string
  students: { id: number; name: string; progress: number; status: string }[]
}

export default function TeacherDashboardPage() {
  const navigate = useNavigate()
  const { token, user, updateUser } = useAuth()
  const [classes, setClasses] = useState<Class[]>([])
  const [assignments, setAssignments] = useState<Assignment[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [showCreateClassDialog, setShowCreateClassDialog] = useState(false)
  const [showJoinDialog, setShowJoinDialog] = useState(false)
  const [classCode, setClassCode] = useState('')
  const [copiedCode, setCopiedCode] = useState(false)

  useEffect(() => {
    if (token) {
      loadTeacherData()
    }
  }, [token])

  const loadTeacherData = async () => {
    try {
      const headers = { Authorization: `Bearer ${token}` }
      
      // Load teacher's classes
      const classesRes = await fetch(`${API_BASE_URL}/api/teacher/my-classes`, { headers })
      const classesData = await classesRes.json()
      if (classesData.success) {
        setClasses(classesData.data || [])
      }

      // Load assignments
      const assignmentsRes = await fetch(`${API_BASE_URL}/api/teacher/assignments`, { headers })
      const assignmentsData = await assignmentsRes.json()
      if (assignmentsData.success) {
        setAssignments(assignmentsData.data || [])
      }
    } catch (error) {
      console.error('Failed to load teacher data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const becomeTeacher = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/user/become-teacher`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
      })
      const data = await response.json()
      
      if (data.success) {
        toast.success('Request sent! Waiting for admin approval.')
        updateUser({ ...user!, teacher_approved: false })
      } else {
        toast.error(data.message || 'Failed to request teacher status')
      }
    } catch (error) {
      toast.error('Failed to request teacher status')
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
        loadTeacherData()
      } else {
        toast.error(data.message || 'Failed to join class')
      }
    } catch (error) {
      toast.error('Failed to join class')
    }
  }

  const copyClassCode = (code: string) => {
    navigator.clipboard.writeText(code)
    setCopiedCode(true)
    setTimeout(() => setCopiedCode(false), 2000)
    toast.success('Class code copied!')
  }

  const userClassCode = user?.class_code

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-muted-foreground">Loading...</div>
      </div>
    )
  }

  // Check if user is a teacher
  const isTeacher = user?.role === 'teacher' || user?.role === 'admin' || user?.role === 'superadmin'
  const isApprovedTeacher = isTeacher && user?.teacher_approved

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border bg-surface">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button variant="ghost" size="icon" onClick={() => navigate('/dashboard')}>
                <ArrowLeft className="h-5 w-5" />
              </Button>
              <GraduationCap className="h-8 w-8 text-primary" />
              <div>
                <h1 className="text-2xl font-heading font-bold">Teacher Dashboard</h1>
                <p className="text-muted-foreground">Manage your classes and assignments</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        {!isApprovedTeacher ? (
          <Card className="max-w-md mx-auto">
            <CardContent className="p-8 text-center">
              <GraduationCap className="h-16 w-16 mx-auto mb-4 text-muted-foreground" />
              <h2 className="text-xl font-heading font-semibold mb-2">Become a Teacher</h2>
              <p className="text-muted-foreground mb-6">
                Request teacher status to create classes and assign courses to students.
              </p>
              <Button onClick={becomeTeacher}>
                <Plus className="h-4 w-4 mr-2" />
                Request Teacher Status
              </Button>
            </CardContent>
          </Card>
        ) : (
          <Tabs defaultValue="classes" className="space-y-6">
            <TabsList>
              <TabsTrigger value="classes">My Classes</TabsTrigger>
              <TabsTrigger value="assignments">Assignments</TabsTrigger>
            </TabsList>

            <TabsContent value="classes" className="space-y-4">
              {/* Class Code Display */}
              {userClassCode && (
                <Card>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="font-semibold text-lg">Your Class Code</h3>
                        <p className="text-sm text-muted-foreground">Share this code with students to join your class</p>
                      </div>
                      <div className="flex items-center gap-2">
                        <code className="bg-muted px-4 py-2 rounded-lg font-mono text-lg">{userClassCode}</code>
                        <Button variant="outline" size="icon" onClick={() => copyClassCode(userClassCode)}>
                          {copiedCode ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Classes List */}
              {classes.length === 0 ? (
                <div className="text-center py-12">
                  <Users className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p className="text-muted-foreground">No classes yet</p>
                </div>
              ) : (
                classes.map((cls) => (
                  <Card key={cls.id}>
                    <CardContent className="p-6">
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="font-semibold">Class {cls.class_code}</h3>
                          <p className="text-sm text-muted-foreground">
                            {cls.student_count || 0} students enrolled
                          </p>
                        </div>
                        <Button variant="outline" size="sm" onClick={() => navigate(`/teacher/class/${cls.class_code}`)}>
                          <Eye className="h-4 w-4 mr-2" />
                          View
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))
              )}
            </TabsContent>

            <TabsContent value="assignments" className="space-y-4">
              {assignments.length === 0 ? (
                <div className="text-center py-12">
                  <BookOpen className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p className="text-muted-foreground">No assignments yet</p>
                </div>
              ) : (
                assignments.map((assignment) => (
                  <Card key={assignment.id}>
                    <CardContent className="p-6">
                      <div className="flex items-start justify-between">
                        <div>
                          <h3 className="font-semibold text-lg">{assignment.course_title}</h3>
                          {assignment.due_date && (
                            <p className="text-sm text-muted-foreground mt-1">
                              Due: {new Date(assignment.due_date).toLocaleDateString()}
                            </p>
                          )}
                        </div>
                        <Button variant="outline" size="sm">
                          <Eye className="h-4 w-4 mr-2" />
                          View Progress
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))
              )}
            </TabsContent>
          </Tabs>
        )}
      </main>
    </div>
  )
}
