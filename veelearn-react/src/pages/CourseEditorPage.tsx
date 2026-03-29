import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useAuth, API_BASE_URL } from '@/context/AuthContext'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { toast } from 'sonner'
import {
  ArrowLeft,
  Save,
  Send,
  Trash2,
  Plus,
  Blocks,
  Code,
  Type,
  Image,
  Link as LinkIcon,
  Play,
  List,
  Layers,
  GripVertical,
  Edit,
  HelpCircle,
  Check,
  X,
  PlusCircle
} from 'lucide-react'

interface Course {
  id: number
  title: string
  description: string
  content: string
  blocks?: string
  status: string
  course_type: 'single' | 'master'
}

interface Unit {
  id: number
  title: string
  order_index: number
  course_id: number
}

interface QuizQuestion {
  id?: number
  question_text: string
  question_type: 'multiple_choice' | 'true_false' | 'short_answer'
  options: string[]
  correct_answer: string
  explanation?: string
  points: number
  order_index?: number
}

export default function CourseEditorPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { token } = useAuth()
  const [course, setCourse] = useState<Course | null>(null)
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [content, setContent] = useState('')
  const [isLoading, setIsLoading] = useState(!!id)
  const [isSaving, setIsSaving] = useState(false)
  const [showUnitDialog, setShowUnitDialog] = useState(false)
  const [units, setUnits] = useState<Unit[]>([])
  const [newUnitTitle, setNewUnitTitle] = useState('')
  const [editingUnit, setEditingUnit] = useState<Unit | null>(null)
  const [availableCourses, setAvailableCourses] = useState<Course[]>([])
  const [showAddUnitDialog, setShowAddUnitDialog] = useState(false)
  const [selectedCourseForUnit, setSelectedCourseForUnit] = useState('')
  
  // Quiz state
  const [showQuizModal, setShowQuizModal] = useState(false)
  const [quizQuestions, setQuizQuestions] = useState<QuizQuestion[]>([])
  const [editingQuestion, setEditingQuestion] = useState<QuizQuestion | null>(null)
  const [questionText, setQuestionText] = useState('')
  const [questionType, setQuestionType] = useState<'multiple_choice' | 'true_false' | 'short_answer'>('multiple_choice')
  const [options, setOptions] = useState<string[]>(['', '', '', ''])
  const [correctAnswer, setCorrectAnswer] = useState('')
  const [explanation, setExplanation] = useState('')
  const [points, setPoints] = useState(10)

  const editorRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (id && token) {
      loadCourse()
    }
  }, [id, token])

  const loadCourse = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/courses/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      const data = await response.json()
      if (data.success) {
        setCourse(data.data)
        setTitle(data.data.title || '')
        setDescription(data.data.description || '')
        setContent(data.data.content || '')
        
        if (data.data.course_type === 'master') {
          loadUnits(data.data.id)
        }
        
        // Load quiz questions
        loadQuizQuestions()
      }
    } catch (error) {
      toast.error('Failed to load course')
      navigate('/dashboard')
    } finally {
      setIsLoading(false)
    }
  }

  const loadUnits = async (courseId: number) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/courses/${courseId}/units`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      const data = await response.json()
      if (data.success) {
        setUnits(data.data || [])
      }
    } catch (error) {
      console.error('Failed to load units:', error)
    }
  }

  const loadQuizQuestions = async () => {
    if (!id) return
    try {
      const response = await fetch(`${API_BASE_URL}/api/courses/${id}/questions`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      const data = await response.json()
      if (data.success) {
        setQuizQuestions(data.data || [])
      }
    } catch (error) {
      console.error('Failed to load quiz questions:', error)
    }
  }

  const loadAvailableCoursesForUnits = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/courses/all?limit=100`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      const data = await response.json()
      if (data.success) {
        setAvailableCourses(data.data || [])
      }
    } catch (error) {
      console.error('Failed to load courses:', error)
    }
  }

  const saveCourse = async (publish: boolean = false) => {
    if (!title.trim()) {
      toast.error('Please enter a course title')
      return
    }

    setIsSaving(true)
    try {
      const endpoint = id 
        ? `${API_BASE_URL}/api/courses/${id}`
        : `${API_BASE_URL}/api/courses`
      
      const method = id ? 'PUT' : 'POST'

      const response = await fetch(endpoint, {
        method,
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          title,
          description,
          content: editorRef.current?.innerHTML || content,
          status: publish ? 'pending' : 'draft',
        }),
      })

      const data = await response.json()

      if (data.success) {
        if (!id) {
          navigate(`/courses/${data.data.id}/edit`, { replace: true })
        }
        toast.success(publish ? 'Course submitted for approval!' : 'Course saved!')
        if (publish) {
          navigate('/dashboard')
        }
      } else {
        toast.error(data.message || 'Failed to save course')
      }
    } catch (error) {
      toast.error('Failed to save course')
    } finally {
      setIsSaving(false)
    }
  }

  const deleteCourse = async () => {
    if (!id) return
    if (!confirm('Are you sure you want to delete this course?')) return

    try {
      const response = await fetch(`${API_BASE_URL}/api/courses/${id}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` },
      })
      const data = await response.json()
      
      if (data.success) {
        toast.success('Course deleted')
        navigate('/dashboard')
      } else {
        toast.error(data.message || 'Failed to delete course')
      }
    } catch (error) {
      toast.error('Failed to delete course')
    }
  }

  const insertAtCursor = (html: string) => {
    const editor = editorRef.current
    if (!editor) return

    editor.focus()
    document.execCommand('insertHTML', false, html)
  }

  const addTextBlock = () => insertAtCursor('<p>Enter your content here...</p>')
  const addHeading = () => insertAtCursor('<h2>New Heading</h2>')
  const addImage = () => {
    const url = prompt('Enter image URL:')
    if (url) insertAtCursor(`<img src="${url}" alt="Image" style="max-width: 100%;" />`)
  }
  const addLink = () => {
    const url = prompt('Enter URL:')
    const text = prompt('Enter link text:')
    if (url && text) insertAtCursor(`<a href="${url}">${text}</a>`)
  }
  const addLatex = () => insertAtCursor('<span class="latex-equation">$E = mc^2$</span>')
  
  const addQuizPlaceholder = () => {
    if (!id) {
      toast.error('Please save the course first before adding quiz questions')
      return
    }
    setShowQuizModal(true)
    resetQuizForm()
  }
  
  const addSimulator = (type: 'block' | 'visual') => {
    const simulatorId = Date.now()
    insertAtCursor(`
      <div class="simulator-placeholder" data-simulator-id="${simulatorId}" data-type="${type}">
        <p style="color: var(--muted-foreground);">[${type === 'block' ? 'Block' : 'Visual'} Simulator]</p>
      </div>
    `)
  }

  // Quiz Functions
  const resetQuizForm = () => {
    setEditingQuestion(null)
    setQuestionText('')
    setQuestionType('multiple_choice')
    setOptions(['', '', '', ''])
    setCorrectAnswer('')
    setExplanation('')
    setPoints(10)
  }

  const openEditQuiz = (question: QuizQuestion) => {
    setEditingQuestion(question)
    setQuestionText(question.question_text)
    setQuestionType(question.question_type)
    setOptions(question.options?.length ? question.options : ['', '', '', ''])
    setCorrectAnswer(question.correct_answer)
    setExplanation(question.explanation || '')
    setPoints(question.points || 10)
    setShowQuizModal(true)
  }

  const saveQuizQuestion = async () => {
    if (!id || !questionText.trim() || !correctAnswer.trim()) {
      toast.error('Please fill in all required fields')
      return
    }

    try {
      const payload = {
        question_text: questionText,
        question_type: questionType,
        options: questionType === 'multiple_choice' ? options.filter(o => o.trim()) : null,
        correct_answer: correctAnswer,
        explanation,
        points,
        order_index: quizQuestions.length
      }

      let response
      if (editingQuestion?.id) {
        response = await fetch(`${API_BASE_URL}/api/courses/${id}/questions/${editingQuestion.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(payload),
        })
      } else {
        response = await fetch(`${API_BASE_URL}/api/courses/${id}/questions`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(payload),
        })
      }

      const data = await response.json()

      if (data.success) {
        toast.success(editingQuestion ? 'Question updated!' : 'Question added!')
        setShowQuizModal(false)
        resetQuizForm()
        loadQuizQuestions()
        
        // Add placeholder to content
        const placeholderHtml = `
          <div class="quiz-question-placeholder" data-question-id="${data.questionId || editingQuestion?.id}">
            <p style="color: var(--muted-foreground);">[Quiz Question]</p>
          </div>
        `
        insertAtCursor(placeholderHtml)
      } else {
        toast.error(data.message || 'Failed to save question')
      }
    } catch (error) {
      toast.error('Failed to save question')
    }
  }

  const deleteQuizQuestion = async (questionId: number) => {
    if (!id || !confirm('Delete this question?')) return

    try {
      const response = await fetch(`${API_BASE_URL}/api/courses/${id}/questions/${questionId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` },
      })

      const data = await response.json()

      if (data.success) {
        toast.success('Question deleted')
        loadQuizQuestions()
      } else {
        toast.error(data.message || 'Failed to delete question')
      }
    } catch (error) {
      toast.error('Failed to delete question')
    }
  }

  const addOption = () => {
    if (options.length < 6) {
      setOptions([...options, ''])
    }
  }

  const updateOption = (index: number, value: string) => {
    const newOptions = [...options]
    newOptions[index] = value
    setOptions(newOptions)
  }

  // Unit Management Functions
  const addUnit = async () => {
    if (!newUnitTitle.trim() || !id) return
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/courses/${id}/units`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ title: newUnitTitle }),
      })
      
      const data = await response.json()
      if (data.success) {
        toast.success('Unit added!')
        setNewUnitTitle('')
        loadUnits(parseInt(id))
      } else {
        toast.error(data.message || 'Failed to add unit')
      }
    } catch (error) {
      toast.error('Failed to add unit')
    }
  }

  const updateUnit = async () => {
    if (!editingUnit || !id) return
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/courses/${id}/units/${editingUnit.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ title: editingUnit.title }),
      })
      
      const data = await response.json()
      if (data.success) {
        toast.success('Unit updated!')
        setEditingUnit(null)
        loadUnits(parseInt(id))
      } else {
        toast.error(data.message || 'Failed to update unit')
      }
    } catch (error) {
      toast.error('Failed to update unit')
    }
  }

  const deleteUnit = async (unitId: number) => {
    if (!id || !confirm('Delete this unit?')) return
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/courses/${id}/units/${unitId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` },
      })
      
      const data = await response.json()
      if (data.success) {
        toast.success('Unit deleted')
        loadUnits(parseInt(id))
      } else {
        toast.error(data.message || 'Failed to delete unit')
      }
    } catch (error) {
      toast.error('Failed to delete unit')
    }
  }

  const addExistingCourseAsUnit = async () => {
    if (!selectedCourseForUnit || !id) return
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/courses/${id}/units`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ 
          title: 'Course Unit',
          linked_course_id: parseInt(selectedCourseForUnit)
        }),
      })
      
      const data = await response.json()
      if (data.success) {
        toast.success('Course added as unit!')
        setShowAddUnitDialog(false)
        setSelectedCourseForUnit('')
        loadUnits(parseInt(id))
      } else {
        toast.error(data.message || 'Failed to add course')
      }
    } catch (error) {
      toast.error('Failed to add course as unit')
    }
  }

  const openBlockSimulator = () => window.open('/block-simulator', '_blank')
  const openVisualSimulator = () => window.open('/visual-simulator', '_blank')

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-muted-foreground">Loading course...</div>
      </div>
    )
  }

  const isMasterCourse = course?.course_type === 'master'

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-surface sticky top-0 z-50">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button variant="ghost" size="icon" onClick={() => navigate('/dashboard')}>
                <ArrowLeft className="h-5 w-5" />
              </Button>
              <div>
                <h1 className="font-heading font-semibold">
                  {id ? 'Edit Course' : 'Create Course'}
                </h1>
                <p className="text-sm text-muted-foreground">
                  {title || 'Untitled Course'} {isMasterCourse && <Layers className="h-3 w-3 inline ml-1" />}
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              {isMasterCourse && (
                <Button variant="outline" size="sm" onClick={() => setShowUnitDialog(true)}>
                  <Layers className="h-4 w-4 mr-2" />
                  Manage Units ({units.length})
                </Button>
              )}
              
              {quizQuestions.length > 0 && (
                <Button variant="outline" size="sm" onClick={() => {
                  resetQuizForm()
                  setShowQuizModal(true)
                }}>
                  <HelpCircle className="h-4 w-4 mr-2" />
                  Quiz ({quizQuestions.length})
                </Button>
              )}
              
              {id && (
                <Button variant="outline" size="sm" onClick={deleteCourse}>
                  <Trash2 className="h-4 w-4" />
                </Button>
              )}
              
              <Button variant="outline" onClick={() => saveCourse(false)} disabled={isSaving}>
                <Save className="h-4 w-4 mr-2" />
                Save Draft
              </Button>
              
              <Button onClick={() => saveCourse(true)} disabled={isSaving}>
                <Send className="h-4 w-4 mr-2" />
                Submit for Approval
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Main Editor */}
          <div className="lg:col-span-3 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Course Details</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="title">Title</Label>
                  <Input id="title" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Enter course title" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="description">Description</Label>
                  <Textarea id="description" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Enter course description" rows={3} />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Content Editor</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Toolbar */}
                <div className="flex flex-wrap gap-2 p-2 bg-muted rounded-lg">
                  <Button variant="ghost" size="sm" onClick={addTextBlock}>
                    <Type className="h-4 w-4 mr-1" /> Text
                  </Button>
                  <Button variant="ghost" size="sm" onClick={addHeading}>
                    <List className="h-4 w-4 mr-1" /> Heading
                  </Button>
                  <Button variant="ghost" size="sm" onClick={addImage}>
                    <Image className="h-4 w-4 mr-1" /> Image
                  </Button>
                  <Button variant="ghost" size="sm" onClick={addLink}>
                    <LinkIcon className="h-4 w-4 mr-1" /> Link
                  </Button>
                  <Button variant="ghost" size="sm" onClick={addLatex}>
                    <span className="mr-1">∑</span> LaTeX
                  </Button>
                  <Button variant="ghost" size="sm" onClick={addQuizPlaceholder}>
                    <HelpCircle className="h-4 w-4 mr-1" /> Quiz
                  </Button>
                  <Button variant="ghost" size="sm" onClick={() => addSimulator('block')}>
                    <Blocks className="h-4 w-4 mr-1" /> Block Sim
                  </Button>
                  <Button variant="ghost" size="sm" onClick={() => addSimulator('visual')}>
                    <Code className="h-4 w-4 mr-1" /> Visual Sim
                  </Button>
                </div>

                {/* Editor Area */}
                <div
                  ref={editorRef}
                  className="min-h-[400px] p-4 border rounded-lg bg-background prose prose-invert max-w-none"
                  contentEditable
                  dangerouslySetInnerHTML={{ __html: content }}
                  onBlur={(e) => setContent(e.currentTarget.innerHTML)}
                  style={{ outline: 'none' }}
                />
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Course Type</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-2">
                  {isMasterCourse ? (
                    <span className="flex items-center gap-2 text-sm">
                      <Layers className="h-4 w-4 text-vee-purple" />
                      Master Course ({units.length} units)
                    </span>
                  ) : (
                    <span className="text-sm text-muted-foreground">Single Course</span>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Quiz Questions List */}
            {quizQuestions.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-base">Quiz Questions ({quizQuestions.length})</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2 max-h-[200px] overflow-y-auto">
                  {quizQuestions.map((q, idx) => (
                    <div key={q.id || idx} className="flex items-center justify-between p-2 bg-muted rounded">
                      <span className="text-sm truncate flex-1">{idx + 1}. {q.question_text}</span>
                      <div className="flex gap-1">
                        <Button variant="ghost" size="sm" onClick={() => openEditQuiz(q)}>
                          <Edit className="h-3 w-3" />
                        </Button>
                        {q.id && (
                          <Button variant="ghost" size="sm" onClick={() => deleteQuizQuestion(q.id!)}>
                            <Trash2 className="h-3 w-3" />
                          </Button>
                        )}
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            )}

            <Card>
              <CardHeader>
                <CardTitle className="text-base">Simulators</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <Button variant="outline" className="w-full justify-start" onClick={openBlockSimulator}>
                  <Blocks className="h-4 w-4 mr-2" /> Block Simulator
                </Button>
                <Button variant="outline" className="w-full justify-start" onClick={openVisualSimulator}>
                  <Code className="h-4 w-4 mr-2" /> Visual Simulator
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-base">Preview</CardTitle>
              </CardHeader>
              <CardContent>
                <Button variant="outline" className="w-full" onClick={() => id && navigate(`/courses/${id}`)} disabled={!id}>
                  <Play className="h-4 w-4 mr-2" /> Preview Course
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      {/* Quiz Modal */}
      <Dialog open={showQuizModal} onOpenChange={setShowQuizModal}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>{editingQuestion ? 'Edit Quiz Question' : 'Add Quiz Question'}</DialogTitle>
            <DialogDescription>
              Create a quiz question for this course
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-4 py-4 max-h-[60vh] overflow-y-auto">
            <div className="space-y-2">
              <Label>Question Text *</Label>
              <Textarea
                value={questionText}
                onChange={(e) => setQuestionText(e.target.value)}
                placeholder="Enter your question here..."
                rows={3}
              />
            </div>

            <div className="space-y-2">
              <Label>Question Type</Label>
              <Select value={questionType} onValueChange={(v) => setQuestionType(v as any)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="multiple_choice">Multiple Choice</SelectItem>
                  <SelectItem value="true_false">True/False</SelectItem>
                  <SelectItem value="short_answer">Short Answer</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {questionType === 'multiple_choice' && (
              <div className="space-y-2">
                <Label>Answer Options</Label>
                {options.map((opt, idx) => (
                  <Input
                    key={idx}
                    value={opt}
                    onChange={(e) => updateOption(idx, e.target.value)}
                    placeholder={`Option ${idx + 1}`}
                  />
                ))}
                {options.length < 6 && (
                  <Button variant="outline" size="sm" onClick={addOption}>
                    <PlusCircle className="h-4 w-4 mr-2" /> Add Option
                  </Button>
                )}
              </div>
            )}

            <div className="space-y-2">
              <Label>Correct Answer *</Label>
              <Input
                value={correctAnswer}
                onChange={(e) => setCorrectAnswer(e.target.value)}
                placeholder={questionType === 'true_false' ? 'True or False' : 'Enter correct answer exactly'}
              />
            </div>

            <div className="space-y-2">
              <Label>Explanation (shown after submission)</Label>
              <Textarea
                value={explanation}
                onChange={(e) => setExplanation(e.target.value)}
                placeholder="Explain why this is the correct answer..."
                rows={2}
              />
            </div>

            <div className="space-y-2">
              <Label>Points</Label>
              <Input
                type="number"
                value={points}
                onChange={(e) => setPoints(parseInt(e.target.value) || 10)}
                min={1}
              />
            </div>
          </div>
          
          <DialogFooter>
            <Button variant="outline" onClick={() => {
              setShowQuizModal(false)
              resetQuizForm()
            }}>
              Cancel
            </Button>
            {editingQuestion?.id && (
              <Button variant="destructive" onClick={() => {
                deleteQuizQuestion(editingQuestion.id!)
                setShowQuizModal(false)
              }}>
                Delete
              </Button>
            )}
            <Button onClick={saveQuizQuestion}>
              {editingQuestion ? 'Update Question' : 'Add Question'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Units Management Dialog */}
      <Dialog open={showUnitDialog} onOpenChange={setShowUnitDialog}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Manage Course Units</DialogTitle>
            <DialogDescription>Add, edit, or reorder units for this master course</DialogDescription>
          </DialogHeader>
          
          <div className="space-y-4 py-4">
            <div className="flex gap-2">
              <Input placeholder="New unit title..." value={newUnitTitle} onChange={(e) => setNewUnitTitle(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && addUnit()} />
              <Button onClick={addUnit}><Plus className="h-4 w-4" /></Button>
            </div>

            <div className="flex gap-2">
              <Button variant="outline" onClick={() => { loadAvailableCoursesForUnits(); setShowAddUnitDialog(true) }}>
                <Plus className="h-4 w-4 mr-2" /> Add Existing Course
              </Button>
            </div>

            <div className="space-y-2 max-h-[300px] overflow-y-auto">
              {units.length === 0 ? (
                <p className="text-center text-muted-foreground py-8">No units yet</p>
              ) : (
                units.map((unit, index) => (
                  <div key={unit.id} className="flex items-center gap-2 p-3 bg-muted rounded-lg">
                    <GripVertical className="h-4 w-4 text-muted-foreground cursor-grab" />
                    <span className="flex-1 font-medium">{unit.title}</span>
                    <Button variant="ghost" size="sm" onClick={() => setEditingUnit(unit)}><Edit className="h-4 w-4" /></Button>
                    <Button variant="ghost" size="sm" onClick={() => deleteUnit(unit.id)}><Trash2 className="h-4 w-4" /></Button>
                  </div>
                ))
              )}
            </div>
          </div>
          
          <DialogFooter><Button variant="outline" onClick={() => setShowUnitDialog(false)}>Close</Button></DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Edit Unit Dialog */}
      <Dialog open={!!editingUnit} onOpenChange={(open) => !open && setEditingUnit(null)}>
        <DialogContent>
          <DialogHeader><DialogTitle>Edit Unit</DialogTitle></DialogHeader>
          <div className="py-4">
            <Input value={editingUnit?.title || ''} onChange={(e) => setEditingUnit(prev => prev ? { ...prev, title: e.target.value } : null)} placeholder="Unit title" />
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setEditingUnit(null)}>Cancel</Button>
            <Button onClick={updateUnit}>Save</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Add Existing Course Dialog */}
      <Dialog open={showAddUnitDialog} onOpenChange={setShowAddUnitDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add Existing Course as Unit</DialogTitle>
            <DialogDescription>Select a course to add as a unit</DialogDescription>
          </DialogHeader>
          <div className="py-4">
            <Select value={selectedCourseForUnit} onValueChange={setSelectedCourseForUnit}>
              <SelectTrigger><SelectValue placeholder="Select a course" /></SelectTrigger>
              <SelectContent>
                {availableCourses.filter(c => c.id !== parseInt(id || '0')).map(course => (
                  <SelectItem key={course.id} value={course.id.toString()}>{course.title}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowAddUnitDialog(false)}>Cancel</Button>
            <Button onClick={addExistingCourseAsUnit}>Add Course</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
