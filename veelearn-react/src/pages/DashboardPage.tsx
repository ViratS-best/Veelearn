import { useState, useEffect, useCallback } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth, API_BASE_URL } from '@/context/AuthContext'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { toast } from 'sonner'
import { 
  BookOpen, 
  Plus, 
  Search, 
  Settings, 
  Users,
  GraduationCap,
  Store,
  LogOut,
  LayoutDashboard,
  Shield,
  ChevronRight,
  Clock,
  Play,
  SortAsc,
  Filter,
  Crown,
  Star
} from 'lucide-react'

interface Course {
  id: number
  title: string
  description: string
  status: 'draft' | 'pending' | 'approved'
  creator_id: number
  creator_email?: string
  created_at: string
  course_type: string
}

type SortOption = 'newest' | 'oldest' | 'title-asc' | 'title-desc'

export default function DashboardPage() {
  const { user, logout, token } = useAuth()
  const navigate = useNavigate()
  const [myCourses, setMyCourses] = useState<Course[]>([])
  const [availableCourses, setAvailableCourses] = useState<Course[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [sortBy, setSortBy] = useState<SortOption>('newest')
  const [showCreateDialog, setShowCreateDialog] = useState(false)
  const [newCourseTitle, setNewCourseTitle] = useState('')
  const [newCourseType, setNewCourseType] = useState<'single' | 'master'>('single')

  const loadCourses = useCallback(async () => {
    if (!token) return
    try {
      const headers = { Authorization: `Bearer ${token}` }
      
      const [myCoursesRes, availableRes] = await Promise.all([
        fetch(`${API_BASE_URL}/api/courses`, { headers }),
        fetch(`${API_BASE_URL}/api/courses/public`, { headers })
      ])

      const myCoursesData = await myCoursesRes.json()
      if (myCoursesData.success) {
        setMyCourses(myCoursesData.data || [])
      }

      const availableData = await availableRes.json()
      if (availableData.success) {
        setAvailableCourses(availableData.data || [])
      }
    } catch (error) {
      console.error('Failed to load courses:', error)
      toast.error('Failed to load courses')
    } finally {
      setIsLoading(false)
    }
  }, [token])

  useEffect(() => {
    loadCourses()
  }, [loadCourses])

  const createCourse = async () => {
    if (!newCourseTitle.trim()) {
      toast.error('Please enter a course title')
      return
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/courses`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          title: newCourseTitle,
          description: '',
          content: '',
          course_type: newCourseType,
        }),
      })

      const data = await response.json()
      
      if (data.success) {
        toast.success('Course created!')
        setShowCreateDialog(false)
        setNewCourseTitle('')
        navigate(`/courses/${data.data.id}/edit`)
      } else {
        toast.error(data.message || 'Failed to create course')
      }
    } catch (error) {
      toast.error('Failed to create course')
    }
  }

  const sortCourses = (courses: Course[]): Course[] => {
    const sorted = [...courses]
    switch (sortBy) {
      case 'newest':
        return sorted.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
      case 'oldest':
        return sorted.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime())
      case 'title-asc':
        return sorted.sort((a, b) => a.title.localeCompare(b.title))
      case 'title-desc':
        return sorted.sort((a, b) => b.title.localeCompare(a.title))
      default:
        return sorted
    }
  }

  const filterCourses = (courses: Course[]) => {
    return courses.filter(c => 
      c.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.description?.toLowerCase().includes(searchQuery.toLowerCase())
    )
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const filteredMyCourses = sortCourses(filterCourses(myCourses))
  const filteredAvailableCourses = sortCourses(filterCourses(availableCourses))

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'approved':
        return <span className="px-2 py-1 text-xs rounded-full bg-green-600/20 text-green-400">Approved</span>
      case 'pending':
        return <span className="px-2 py-1 text-xs rounded-full bg-yellow-600/20 text-yellow-400">Pending</span>
      default:
        return <span className="px-2 py-1 text-xs rounded-full bg-gray-600/20 text-gray-400">Draft</span>
    }
  }

  const getCourseTypeBadge = (type: string) => {
    if (type === 'master') {
      return <span className="px-2 py-1 text-xs rounded-full bg-vee-purple/20 text-vee-purple">Master</span>
    }
    return null
  }

  const isSuperadmin = user?.role === 'superadmin'
  const isAdmin = user?.role === 'admin' || isSuperadmin
  const isTeacher = user?.role === 'teacher' || isAdmin

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-surface">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <h1 className="text-2xl font-heading font-bold text-highlight">Veelearn</h1>
              <span className="text-muted-foreground">|</span>
              <span className="text-sm text-muted-foreground">Welcome, {user?.name}</span>
              {isSuperadmin && (
                <span className="px-2 py-1 text-xs rounded-full bg-yellow-600/20 text-yellow-400 flex items-center gap-1">
                  <Crown className="h-3 w-3" /> Superadmin
                </span>
              )}
            </div>
            
            <div className="flex items-center gap-2">
              {isAdmin && (
                <Button variant="ghost" size="sm" asChild>
                  <Link to="/admin">
                    <Shield className="h-4 w-4 mr-2" />
                    Admin
                  </Link>
                </Button>
              )}
              
              {isTeacher && (
                <Button variant="ghost" size="sm" asChild>
                  <Link to="/teacher">
                    <GraduationCap className="h-4 w-4 mr-2" />
                    Teacher
                  </Link>
                </Button>
              )}

              <Button variant="ghost" size="sm" asChild>
                <Link to="/student">
                  <Users className="h-4 w-4 mr-2" />
                  Student
                </Link>
              </Button>

              <Button variant="ghost" size="sm" asChild>
                <Link to="/marketplace">
                  <Store className="h-4 w-4 mr-2" />
                  Marketplace
                </Link>
              </Button>

              <Button variant="ghost" size="sm" onClick={handleLogout}>
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
            <DialogTrigger asChild>
              <Card className="cursor-pointer hover:bg-accent/10 transition-colors border-highlight/20">
                <CardContent className="p-6 flex items-center gap-4">
                  <div className="h-12 w-12 rounded-lg bg-highlight/20 flex items-center justify-center">
                    <Plus className="h-6 w-6 text-highlight" />
                  </div>
                  <div>
                    <h3 className="font-semibold">Create Course</h3>
                    <p className="text-sm text-muted-foreground">Start a new course</p>
                  </div>
                </CardContent>
              </Card>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Create New Course</DialogTitle>
                <DialogDescription>
                  Choose between a single course or a master course with multiple units
                </DialogDescription>
              </DialogHeader>
              <div className="space-y-4 py-4">
                <div className="space-y-2">
                  <Label htmlFor="course-title">Course Title</Label>
                  <Input
                    id="course-title"
                    placeholder="Enter course title"
                    value={newCourseTitle}
                    onChange={(e) => setNewCourseTitle(e.target.value)}
                  />
                </div>
                <div className="space-y-2">
                  <Label>Course Type</Label>
                  <div className="grid grid-cols-2 gap-2">
                    <Button
                      variant={newCourseType === 'single' ? 'default' : 'outline'}
                      onClick={() => setNewCourseType('single')}
                    >
                      Single Course
                    </Button>
                    <Button
                      variant={newCourseType === 'master' ? 'default' : 'outline'}
                      onClick={() => setNewCourseType('master')}
                    >
                      Master Course
                    </Button>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    {newCourseType === 'single' 
                      ? 'A standalone course with lessons and content' 
                      : 'A parent course that contains multiple units (sub-courses)'}
                  </p>
                </div>
              </div>
              <DialogFooter>
                <Button variant="outline" onClick={() => setShowCreateDialog(false)}>
                  Cancel
                </Button>
                <Button onClick={createCourse}>Create Course</Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>

          <Card className="cursor-pointer hover:bg-accent/10 transition-colors" onClick={() => navigate('/courses/new')}>
            <CardContent className="p-6 flex items-center gap-4">
              <div className="h-12 w-12 rounded-lg bg-primary/20 flex items-center justify-center">
                <LayoutDashboard className="h-6 w-6 text-primary" />
              </div>
              <div>
                <h3 className="font-semibold">Course Editor</h3>
                <p className="text-sm text-muted-foreground">Design courses</p>
              </div>
            </CardContent>
          </Card>

          <Card className="cursor-pointer hover:bg-accent/10 transition-colors" onClick={() => navigate('/marketplace')}>
            <CardContent className="p-6 flex items-center gap-4">
              <div className="h-12 w-12 rounded-lg bg-vee-purple/20 flex items-center justify-center">
                <Store className="h-6 w-6 text-vee-purple" />
              </div>
              <div>
                <h3 className="font-semibold">Simulator Marketplace</h3>
                <p className="text-sm text-muted-foreground">Browse & share</p>
              </div>
            </CardContent>
          </Card>

          <Card className="cursor-pointer hover:bg-accent/10 transition-colors" onClick={() => navigate('/block-simulator')}>
            <CardContent className="p-6 flex items-center gap-4">
              <div className="h-12 w-12 rounded-lg bg-vee-aqua/20 flex items-center justify-center">
                <Settings className="h-6 w-6 text-vee-aqua" />
              </div>
              <div>
                <h3 className="font-semibold">Block Simulator</h3>
                <p className="text-sm text-muted-foreground">Create simulations</p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Courses Tabs */}
        <Tabs defaultValue="my-courses" className="space-y-4">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <TabsList>
              <TabsTrigger value="my-courses">My Courses ({filteredMyCourses.length})</TabsTrigger>
              <TabsTrigger value="available">Available ({filteredAvailableCourses.length})</TabsTrigger>
            </TabsList>

            <div className="flex items-center gap-2">
              <div className="relative w-64">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search courses..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-9"
                />
              </div>
              
              <Select value={sortBy} onValueChange={(v) => setSortBy(v as SortOption)}>
                <SelectTrigger className="w-[150px]">
                  <SortAsc className="h-4 w-4 mr-2" />
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="newest">Newest First</SelectItem>
                  <SelectItem value="oldest">Oldest First</SelectItem>
                  <SelectItem value="title-asc">Title (A-Z)</SelectItem>
                  <SelectItem value="title-desc">Title (Z-A)</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <TabsContent value="my-courses" className="space-y-4">
            {isLoading ? (
              <div className="text-center py-8 text-muted-foreground">Loading courses...</div>
            ) : filteredMyCourses.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                <BookOpen className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>No courses yet. Create your first course!</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {filteredMyCourses.map((course) => (
                  <Card key={course.id} className="hover:bg-accent/5 transition-colors">
                    <CardHeader className="pb-2">
                      <div className="flex items-start justify-between gap-2">
                        <CardTitle className="text-lg line-clamp-1">{course.title}</CardTitle>
                        <div className="flex gap-1">
                          {getCourseTypeBadge(course.course_type)}
                          {getStatusBadge(course.status)}
                        </div>
                      </div>
                      <CardDescription className="line-clamp-2">
                        {course.description || 'No description'}
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="flex items-center justify-between text-sm text-muted-foreground">
                        <div className="flex items-center gap-1">
                          <Clock className="h-3 w-3" />
                          {new Date(course.created_at).toLocaleDateString()}
                        </div>
                        <div className="flex gap-2">
                          <Button 
                            variant="ghost" 
                            size="sm"
                            onClick={() => navigate(`/courses/${course.id}/edit`)}
                          >
                            Edit
                          </Button>
                          <Button 
                            variant="ghost" 
                            size="sm"
                            onClick={() => navigate(`/courses/${course.id}`)}
                          >
                            <Play className="h-3 w-3 mr-1" />
                            View
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </TabsContent>

          <TabsContent value="available" className="space-y-4">
            {isLoading ? (
              <div className="text-center py-8 text-muted-foreground">Loading courses...</div>
            ) : filteredAvailableCourses.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                <BookOpen className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>No available courses found</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {filteredAvailableCourses.map((course) => (
                  <Card key={course.id} className="hover:bg-accent/5 transition-colors">
                    <CardHeader className="pb-2">
                      <div className="flex items-start justify-between gap-2">
                        <CardTitle className="text-lg line-clamp-1">{course.title}</CardTitle>
                        {getCourseTypeBadge(course.course_type)}
                      </div>
                      <CardDescription className="line-clamp-2">
                        {course.description || 'No description'}
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="flex items-center justify-between text-sm text-muted-foreground">
                        <div className="flex items-center gap-1">
                          <Users className="h-3 w-3" />
                          {course.creator_email}
                        </div>
                        <Button 
                          variant="ghost" 
                          size="sm"
                          onClick={() => navigate(`/courses/${course.id}`)}
                        >
                          <Play className="h-3 w-3 mr-1" />
                          Start
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}
