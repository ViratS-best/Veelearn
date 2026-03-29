import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth, API_BASE_URL } from '@/context/AuthContext'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { toast } from 'sonner'
import {
  ArrowLeft,
  Users,
  BookOpen,
  Shield,
  Check,
  X,
  Trash2,
  Search,
  UserCog,
  Crown,
  GraduationCap,
  Settings,
  Eye,
  Edit
} from 'lucide-react'

interface User {
  id: number
  name: string
  email: string
  role: string
  teacher_approved?: boolean
  class_code?: string
  created_at: string
}

interface Course {
  id: number
  title: string
  description: string
  status: string
  course_type: string
  creator_email: string
  created_at: string
}

interface PendingTeacher {
  id: number
  name: string
  email: string
  created_at: string
}

export default function AdminPanelPage() {
  const navigate = useNavigate()
  const { token, user } = useAuth()
  const [users, setUsers] = useState<User[]>([])
  const [courses, setCourses] = useState<Course[]>([])
  const [pendingCourses, setPendingCourses] = useState<Course[]>([])
  const [pendingTeachers, setPendingTeachers] = useState<PendingTeacher[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedUser, setSelectedUser] = useState<User | null>(null)
  const [showUserDetails, setShowUserDetails] = useState(false)

  const isSuperadmin = user?.role === 'superadmin'

  useEffect(() => {
    if (token) {
      loadData()
    }
  }, [token])

  const loadData = async () => {
    try {
      const headers = { Authorization: `Bearer ${token}` }
      
      // Load all users
      const usersRes = await fetch(`${API_BASE_URL}/api/users`, { headers })
      const usersData = await usersRes.json()
      if (usersData.success) {
        setUsers(usersData.data || [])
      }

      // Load pending courses
      const pendingRes = await fetch(`${API_BASE_URL}/api/admin/courses/pending`, { headers })
      const pendingData = await pendingRes.json()
      if (pendingData.success) {
        setPendingCourses(pendingData.data || [])
      }

      // Load all courses
      const coursesRes = await fetch(`${API_BASE_URL}/api/courses`, { headers })
      const coursesData = await coursesRes.json()
      if (coursesData.success) {
        setCourses(coursesData.data || [])
      }

      // Load pending teacher requests (if superadmin)
      if (isSuperadmin) {
        try {
          const teachersRes = await fetch(`${API_BASE_URL}/api/admin/pending-teachers`, { headers })
          const teachersData = await teachersRes.json()
          if (teachersData.success) {
            setPendingTeachers(teachersData.data || [])
          }
        } catch (e) {
          console.error('Failed to load pending teachers:', e)
        }
      }
    } catch (error) {
      toast.error('Failed to load admin data')
    } finally {
      setIsLoading(false)
    }
  }

  const changeUserRole = async (userId: number, newRole: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/users/${userId}/role`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ role: newRole }),
      })

      const data = await response.json()
      if (data.success) {
        toast.success(`User role updated to ${newRole}`)
        loadData()
      } else {
        toast.error(data.message || 'Failed to update role')
      }
    } catch (error) {
      toast.error('Failed to update role')
    }
  }

  const approveTeacher = async (userId: number) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/approve-teacher/${userId}`, {
        method: 'PUT',
        headers: { Authorization: `Bearer ${token}` },
      })
      
      const data = await response.json()
      if (data.success) {
        toast.success('Teacher approved!')
        loadData()
      } else {
        toast.error(data.message || 'Failed to approve teacher')
      }
    } catch (error) {
      toast.error('Failed to approve teacher')
    }
  }

  const approveCourse = async (courseId: number) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/courses/${courseId}/status`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ status: 'approved' }),
      })

      const data = await response.json()
      if (data.success) {
        toast.success('Course approved!')
        loadData()
      } else {
        toast.error(data.message || 'Failed to approve')
      }
    } catch (error) {
      toast.error('Failed to approve course')
    }
  }

  const rejectCourse = async (courseId: number) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/courses/${courseId}/status`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ status: 'rejected' }),
      })

      const data = await response.json()
      if (data.success) {
        toast.success('Course rejected')
        loadData()
      } else {
        toast.error(data.message || 'Failed to reject')
      }
    } catch (error) {
      toast.error('Failed to reject course')
    }
  }

  const deleteCourse = async (courseId: number) => {
    if (!confirm('Are you sure you want to delete this course?')) return

    try {
      const response = await fetch(`${API_BASE_URL}/api/courses/${courseId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` },
      })
      const data = await response.json()
      
      if (data.success) {
        toast.success('Course deleted')
        loadData()
      } else {
        toast.error(data.message || 'Failed to delete')
      }
    } catch (error) {
      toast.error('Failed to delete course')
    }
  }

  const deleteUser = async (userId: number) => {
    if (!confirm('Are you sure you want to delete this user?')) return

    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/users/${userId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` },
      })
      const data = await response.json()
      
      if (data.success) {
        toast.success('User deleted')
        loadData()
      } else {
        toast.error(data.message || 'Failed to delete user')
      }
    } catch (error) {
      toast.error('Failed to delete user')
    }
  }

  const filteredUsers = users.filter(u => 
    u.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    u.email.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const filteredCourses = courses.filter(c =>
    c.title.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const getRoleBadge = (role: string) => {
    switch (role) {
      case 'superadmin':
        return <span className="px-2 py-1 text-xs rounded-full bg-yellow-600/20 text-yellow-400 flex items-center gap-1">
          <Crown className="h-3 w-3" /> Superadmin
        </span>
      case 'admin':
        return <span className="px-2 py-1 text-xs rounded-full bg-red-600/20 text-red-400 flex items-center gap-1">
          <Shield className="h-3 w-3" /> Admin
        </span>
      case 'teacher':
        return <span className="px-2 py-1 text-xs rounded-full bg-blue-600/20 text-blue-400 flex items-center gap-1">
          <GraduationCap className="h-3 w-3" /> Teacher
        </span>
      default:
        return <span className="px-2 py-1 text-xs rounded-full bg-gray-600/20 text-gray-400">User</span>
    }
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
              <Shield className="h-8 w-8 text-primary" />
              <div>
                <h1 className="text-2xl font-heading font-bold">Admin Panel</h1>
                <p className="text-muted-foreground">
                  {isSuperadmin ? 'Superadmin Dashboard' : 'Admin Dashboard'}
                </p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <Input
            placeholder="Search users and courses..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="max-w-md"
          />
        </div>

        <Tabs defaultValue="pending" className="space-y-6">
          <TabsList>
            {isSuperadmin && (
              <TabsTrigger value="teachers">
                Teacher Requests ({pendingTeachers.length})
              </TabsTrigger>
            )}
            <TabsTrigger value="pending">
              Pending Courses ({pendingCourses.length})
            </TabsTrigger>
            <TabsTrigger value="courses">
              All Courses ({filteredCourses.length})
            </TabsTrigger>
            <TabsTrigger value="users">
              Users ({filteredUsers.length})
            </TabsTrigger>
          </TabsList>

          {isSuperadmin && (
            <TabsContent value="teachers" className="space-y-4">
              {isLoading ? (
                <div className="text-center py-8 text-muted-foreground">Loading...</div>
              ) : pendingTeachers.length === 0 ? (
                <div className="text-center py-12">
                  <GraduationCap className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p className="text-muted-foreground">No pending teacher requests</p>
                </div>
              ) : (
                pendingTeachers.map((teacher) => (
                  <Card key={teacher.id}>
                    <CardContent className="p-6">
                      <div className="flex items-start justify-between">
                        <div className="flex items-center gap-4">
                          <div className="h-12 w-12 rounded-full bg-primary/20 flex items-center justify-center">
                            <UserCog className="h-6 w-6" />
                          </div>
                          <div>
                            <h3 className="font-semibold text-lg">{teacher.name}</h3>
                            <p className="text-muted-foreground">{teacher.email}</p>
                            <p className="text-sm text-muted-foreground mt-1">
                              Requested: {new Date(teacher.created_at).toLocaleDateString()}
                            </p>
                          </div>
                        </div>
                        <div className="flex gap-2">
                          <Button size="sm" onClick={() => approveTeacher(teacher.id)}>
                            <Check className="h-4 w-4 mr-1" />
                            Approve
                          </Button>
                          <Button variant="outline" size="sm" onClick={() => deleteUser(teacher.id)}>
                            <X className="h-4 w-4 mr-1" />
                            Reject
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))
              )}
            </TabsContent>
          )}

          <TabsContent value="pending" className="space-y-4">
            {isLoading ? (
              <div className="text-center py-8 text-muted-foreground">Loading...</div>
            ) : pendingCourses.length === 0 ? (
              <div className="text-center py-12">
                <BookOpen className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p className="text-muted-foreground">No pending courses</p>
              </div>
            ) : (
              pendingCourses.map((course) => (
                <Card key={course.id}>
                  <CardContent className="p-6">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <h3 className="font-semibold text-lg">{course.title}</h3>
                          {course.course_type === 'master' && (
                            <span className="px-2 py-1 text-xs rounded-full bg-vee-purple/20 text-vee-purple">Master</span>
                          )}
                        </div>
                        <p className="text-muted-foreground mt-1">{course.description}</p>
                        <p className="text-sm text-muted-foreground mt-2">
                          By {course.creator_email} • {new Date(course.created_at).toLocaleDateString()}
                        </p>
                      </div>
                      <div className="flex gap-2 ml-4">
                        <Button size="sm" variant="outline" onClick={() => navigate(`/courses/${course.id}`)}>
                          <Eye className="h-4 w-4 mr-1" />
                          Preview
                        </Button>
                        <Button size="sm" onClick={() => approveCourse(course.id)}>
                          <Check className="h-4 w-4 mr-1" />
                          Approve
                        </Button>
                        <Button variant="outline" size="sm" onClick={() => rejectCourse(course.id)}>
                          <X className="h-4 w-4 mr-1" />
                          Reject
                        </Button>
                        <Button variant="ghost" size="sm" onClick={() => deleteCourse(course.id)}>
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </TabsContent>

          <TabsContent value="courses" className="space-y-4">
            {filteredCourses.length === 0 ? (
              <div className="text-center py-12 text-muted-foreground">No courses found</div>
            ) : (
              filteredCourses.map((course) => (
                <Card key={course.id}>
                  <CardContent className="p-6">
                    <div className="flex items-start justify-between">
                      <div>
                        <div className="flex items-center gap-2">
                          <h3 className="font-semibold">{course.title}</h3>
                          {course.course_type === 'master' && (
                            <span className="px-2 py-1 text-xs rounded-full bg-vee-purple/20 text-vee-purple">Master</span>
                          )}
                        </div>
                        <p className="text-sm text-muted-foreground">{course.creator_email}</p>
                      </div>
                      <div className="flex items-center gap-4">
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          course.status === 'approved' ? 'bg-green-600/20 text-green-400' :
                          course.status === 'pending' ? 'bg-yellow-600/20 text-yellow-400' :
                          'bg-gray-600/20 text-gray-400'
                        }`}>
                          {course.status}
                        </span>
                        <Button variant="ghost" size="sm" onClick={() => navigate(`/courses/${course.id}/edit`)}>
                          <Edit className="h-4 w-4 mr-1" />
                          Edit
                        </Button>
                        <Button variant="ghost" size="sm" onClick={() => deleteCourse(course.id)}>
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </TabsContent>

          <TabsContent value="users" className="space-y-4">
            {filteredUsers.length === 0 ? (
              <div className="text-center py-12 text-muted-foreground">No users found</div>
            ) : (
              filteredUsers.map((u) => (
                <Card key={u.id}>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <div className="h-10 w-10 rounded-full bg-primary/20 flex items-center justify-center">
                          <UserCog className="h-5 w-5" />
                        </div>
                        <div>
                          <h3 className="font-semibold">{u.name}</h3>
                          <p className="text-sm text-muted-foreground">{u.email}</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-4">
                        {getRoleBadge(u.role)}
                        <Select value={u.role} onValueChange={(newRole) => changeUserRole(u.id, newRole)}>
                          <SelectTrigger className="w-[130px]">
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="user">User</SelectItem>
                            <SelectItem value="teacher">Teacher</SelectItem>
                            <SelectItem value="admin">Admin</SelectItem>
                            {isSuperadmin && (
                              <SelectItem value="superadmin">Superadmin</SelectItem>
                            )}
                          </SelectContent>
                        </Select>
                        <Button variant="ghost" size="sm" onClick={() => deleteUser(u.id)}>
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}
