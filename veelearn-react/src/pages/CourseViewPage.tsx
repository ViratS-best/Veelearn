import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useAuth, API_BASE_URL } from '@/context/AuthContext'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { Label } from '@/components/ui/label'
import { Progress } from '@/components/ui/progress'
import { toast } from 'sonner'
import {
  ArrowLeft,
  Play,
  Users,
  BookOpen,
  Layers,
  ChevronRight,
  CheckCircle,
  Clock,
  XCircle,
  HelpCircle
} from 'lucide-react'

interface Course {
  id: number
  title: string
  description: string
  content: string
  status: string
  course_type: string
  creator_id: number
  creator_email?: string
  created_at: string
}

interface Unit {
  id: number
  title: string
  order_index: number
  course_id: number
}

interface QuizQuestion {
  id: number
  question_text: string
  question_type: string
  options: string[] | null
  correct_answer: string
  explanation?: string
  points?: number
}

interface QuizAnswer {
  question_id: number
  selected_answer: string
  is_correct: boolean
  explanation?: string
}

export default function CourseViewPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { token, user } = useAuth()
  const [course, setCourse] = useState<Course | null>(null)
  const [units, setUnits] = useState<Unit[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isEnrolled, setIsEnrolled] = useState(false)
  
  // Quiz state
  const [questions, setQuestions] = useState<QuizQuestion[]>([])
  const [quizAnswers, setQuizAnswers] = useState<QuizAnswer[]>([])
  const [showQuiz, setShowQuiz] = useState(false)
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [quizSubmitted, setQuizSubmitted] = useState(false)
  const [score, setScore] = useState(0)

  useEffect(() => {
    if (id && token) {
      loadCourse()
      checkEnrollment()
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
        
        if (data.data.course_type === 'master') {
          const unitsRes = await fetch(`${API_BASE_URL}/api/courses/${id}/units`, {
            headers: { Authorization: `Bearer ${token}` },
          })
          const unitsData = await unitsRes.json()
          if (unitsData.success) {
            setUnits(unitsData.data || [])
          }
        }

        // Load quiz questions
        const questionsRes = await fetch(`${API_BASE_URL}/api/courses/${id}/questions`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        const questionsData = await questionsRes.json()
        if (questionsData.success && questionsData.data) {
          setQuestions(questionsData.data)
        }
      }
    } catch (error) {
      toast.error('Failed to load course')
    } finally {
      setIsLoading(false)
    }
  }

  const checkEnrollment = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/users/enrollments`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      const data = await response.json()
      
      if (data.success) {
        const enrollments = data.data || []
        setIsEnrolled(enrollments.some((e: any) => e.course_id === parseInt(id!)))
      }
    } catch (error) {
      console.error('Failed to check enrollment:', error)
    }
  }

  const enrollInCourse = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/courses/${id}/enroll`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
      })
      const data = await response.json()
      
      if (data.success) {
        setIsEnrolled(true)
        toast.success('Enrolled in course!')
      } else {
        toast.error(data.message || 'Failed to enroll')
      }
    } catch (error) {
      toast.error('Failed to enroll')
    }
  }

  const startLearning = () => {
    if (questions.length > 0) {
      setShowQuiz(true)
      setCurrentQuestion(0)
      setQuizAnswers([])
      setQuizSubmitted(false)
    } else {
      navigate(`/player/${id}`)
    }
  }

  const handleAnswerSelect = (answer: string) => {
    if (quizSubmitted) return
    
    const question = questions[currentQuestion]
    const existingIndex = quizAnswers.findIndex(a => a.question_id === question.id)
    
    const isCorrect = answer.trim().toLowerCase() === question.correct_answer.trim().toLowerCase()
    
    const newAnswer: QuizAnswer = {
      question_id: question.id,
      selected_answer: answer,
      is_correct: isCorrect,
      explanation: question.explanation
    }
    
    if (existingIndex >= 0) {
      const updated = [...quizAnswers]
      updated[existingIndex] = newAnswer
      setQuizAnswers(updated)
    } else {
      setQuizAnswers([...quizAnswers, newAnswer])
    }
  }

  const nextQuestion = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(prev => prev + 1)
    }
  }

  const prevQuestion = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(prev => prev - 1)
    }
  }

  const submitQuiz = async () => {
    const correct = quizAnswers.filter(a => a.is_correct).length
    const percentage = Math.round((correct / questions.length) * 100)
    setScore(percentage)
    setQuizSubmitted(true)

    // Submit each answer to the API and get feedback
    for (const answer of quizAnswers) {
      try {
        const response = await fetch(`${API_BASE_URL}/api/courses/${id}/questions/${answer.question_id}/answer`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ user_answer: answer.selected_answer }),
        })
        const data = await response.json()
        if (data.success && data.data) {
          // Update the answer with explanation from server
          const updatedAnswers = quizAnswers.map(a => 
            a.question_id === answer.question_id 
              ? { ...a, explanation: data.data.explanation }
              : a
          )
          setQuizAnswers(updatedAnswers)
        }
      } catch (error) {
        console.error('Failed to submit answer:', error)
      }
    }

    toast.info(`Quiz completed! Score: ${percentage}%`)
  }

  const getAnswerState = (answerOption: string) => {
    const answer = quizAnswers.find(a => a.question_id === questions[currentQuestion].id)
    const question = questions[currentQuestion]
    if (!answer) return 'unanswered'
    
    const isSelected = answer.selected_answer.trim().toLowerCase() === answerOption.trim().toLowerCase()
    const isCorrectAnswer = question.correct_answer?.trim().toLowerCase() === answerOption.trim().toLowerCase()
    
    if (isSelected) {
      return answer.is_correct ? 'correct' : 'incorrect'
    }
    if (quizSubmitted && isCorrectAnswer) {
      return 'correct-answer'
    }
    return 'unanswered'
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-muted-foreground">Loading course...</div>
      </div>
    )
  }

  if (!course) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <p className="text-muted-foreground mb-4">Course not found</p>
          <Button onClick={() => navigate('/dashboard')}>Go to Dashboard</Button>
        </div>
      </div>
    )
  }

  // Quiz Mode
  if (showQuiz && questions.length > 0) {
    const question = questions[currentQuestion]

    return (
      <div className="min-h-screen bg-background">
        <header className="border-b border-border bg-surface">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center gap-4">
              <Button variant="ghost" size="icon" onClick={() => setShowQuiz(false)}>
                <ArrowLeft className="h-5 w-5" />
              </Button>
              <div>
                <h1 className="font-heading font-semibold text-xl">{course.title}</h1>
                <p className="text-sm text-muted-foreground">Quiz - Question {currentQuestion + 1} of {questions.length}</p>
              </div>
            </div>
          </div>
        </header>

        <main className="container mx-auto px-4 py-8">
          <div className="max-w-2xl mx-auto">
            <Progress value={((currentQuestion + 1) / questions.length) * 100} className="mb-8" />

            <Card>
              <CardHeader>
                <CardTitle className="text-xl">{question.question_text}</CardTitle>
              </CardHeader>
              <CardContent>
                <RadioGroup 
                  value={quizAnswers.find(a => a.question_id === question.id)?.selected_answer || ''}
                  onValueChange={(v) => handleAnswerSelect(v)}
                  disabled={quizSubmitted}
                >
                  {(question.options || []).map((option, index) => {
                    const state = getAnswerState(option)
                    return (
                    <div 
                      key={index}
                      className={`flex items-center space-x-2 p-4 rounded-lg border mb-2 transition-colors ${
                        state === 'correct' ? 'bg-green-600/20 border-green-600' :
                        state === 'incorrect' ? 'bg-red-600/20 border-red-600' :
                        state === 'correct-answer' ? 'bg-green-600/20 border-green-600' :
                        'border-input hover:bg-accent'
                      }`}
                    >
                      <RadioGroupItem value={option} id={`option-${index}`} />
                      <Label htmlFor={`option-${index}`} className="flex-1 cursor-pointer">
                        {option}
                      </Label>
                      {state === 'correct' && <CheckCircle className="h-5 w-5 text-green-500" />}
                      {state === 'incorrect' && <XCircle className="h-5 w-5 text-red-500" />}
                      {quizSubmitted && state === 'correct-answer' && <CheckCircle className="h-5 w-5 text-green-500" />}
                    </div>
                  )})}
                  {question.question_type === 'short_answer' && (
                    <div className="mt-4">
                      <Input 
                        placeholder="Type your answer..."
                        value={quizAnswers.find(a => a.question_id === question.id)?.selected_answer || ''}
                        onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleAnswerSelect(e.target.value)}
                        disabled={quizSubmitted}
                      />
                    </div>
                  )}
                  {question.question_type === 'true_false' && (
                    <>
                      {['True', 'False'].map((option) => {
                        const state = getAnswerState(option)
                        return (
                        <div 
                          key={option}
                          className={`flex items-center space-x-2 p-4 rounded-lg border mb-2 transition-colors ${
                            state === 'correct' ? 'bg-green-600/20 border-green-600' :
                            state === 'incorrect' ? 'bg-red-600/20 border-red-600' :
                            state === 'correct-answer' ? 'bg-green-600/20 border-green-600' :
                            'border-input hover:bg-accent'
                          }`}
                        >
                          <RadioGroupItem value={option} id={`option-${option}`} />
                          <Label htmlFor={`option-${option}`} className="flex-1 cursor-pointer">
                            {option}
                          </Label>
                          {state === 'correct' && <CheckCircle className="h-5 w-5 text-green-500" />}
                          {state === 'incorrect' && <XCircle className="h-5 w-5 text-red-500" />}
                          {quizSubmitted && state === 'correct-answer' && <CheckCircle className="h-5 w-5 text-green-500" />}
                        </div>
                      )})}
                    </>
                  )}
                </RadioGroup>

                <div className="flex justify-between mt-6">
                  <Button variant="outline" onClick={prevQuestion} disabled={currentQuestion === 0}>
                    Previous
                  </Button>
                  
                  {currentQuestion < questions.length - 1 ? (
                    <Button onClick={nextQuestion} disabled={!quizAnswers.find(a => a.question_id === question.id)}>
                      Next
                    </Button>
                  ) : (
                    <Button onClick={submitQuiz} disabled={quizAnswers.length !== questions.length}>
                      Submit Quiz
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>

            {quizSubmitted && (
              <Card className="mt-6">
                <CardContent className="p-6 text-center">
                  <h3 className="text-2xl font-heading font-bold mb-2">Quiz Complete!</h3>
                  <p className="text-4xl font-bold text-highlight mb-4">{score}%</p>
                  <p className="text-muted-foreground">
                    You got {quizAnswers.filter(a => a.is_correct).length} out of {questions.length} correct
                  </p>
                  <div className="flex gap-2 justify-center mt-4">
                    <Button variant="outline" onClick={() => {
                      setShowQuiz(false)
                      navigate(`/player/${id}`)
                    }}>
                      Continue Course
                    </Button>
                    <Button onClick={() => {
                      setQuizAnswers([])
                      setCurrentQuestion(0)
                      setQuizSubmitted(false)
                      setScore(0)
                    }}>
                      Retry Quiz
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </main>
      </div>
    )
  }

  // Normal Course View
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-surface">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon" onClick={() => navigate(-1)}>
              <ArrowLeft className="h-5 w-5" />
            </Button>
            <div>
              <h1 className="font-heading font-semibold text-xl">{course.title}</h1>
              <p className="text-sm text-muted-foreground">
                By {course.creator_email}
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Course Hero */}
            <Card>
              <CardContent className="p-6">
                <h2 className="text-2xl font-heading font-bold mb-4">{course.title}</h2>
                <p className="text-muted-foreground mb-4">{course.description}</p>
                
                <div className="flex items-center gap-4 text-sm text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <Clock className="h-4 w-4" />
                    {new Date(course.created_at).toLocaleDateString()}
                  </div>
                  {course.course_type === 'master' && (
                    <div className="flex items-center gap-1">
                      <Layers className="h-4 w-4" />
                      {units.length} Units
                    </div>
                  )}
                  {questions.length > 0 && (
                    <div className="flex items-center gap-1">
                      <HelpCircle className="h-4 w-4" />
                      {questions.length} Quiz Questions
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Course Content */}
            <Card>
              <CardHeader>
                <CardTitle>Course Content</CardTitle>
              </CardHeader>
              <CardContent>
                {course.course_type === 'master' && units.length > 0 ? (
                  <div className="space-y-2">
                    {units.map((unit, index) => (
                      <div
                        key={unit.id}
                        className="flex items-center gap-3 p-3 rounded-lg bg-muted hover:bg-muted/80 cursor-pointer"
                      >
                        <div className="h-8 w-8 rounded-full bg-primary/20 flex items-center justify-center text-sm font-medium">
                          {index + 1}
                        </div>
                        <span className="flex-1">{unit.title}</span>
                        <ChevronRight className="h-4 w-4 text-muted-foreground" />
                      </div>
                    ))}
                  </div>
                ) : (
                  <div 
                    className="prose prose-invert max-w-none"
                    dangerouslySetInnerHTML={{ __html: course.content || '<p>No content available</p>' }}
                  />
                )}
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-4">
            {/* Enrollment Card */}
            <Card>
              <CardContent className="p-6">
                {isEnrolled ? (
                  <div className="space-y-4">
                    <div className="flex items-center gap-2 text-green-400">
                      <CheckCircle className="h-5 w-5" />
                      <span className="font-medium">Enrolled</span>
                    </div>
                    <Button className="w-full" onClick={startLearning}>
                      <Play className="h-4 w-4 mr-2" />
                      {questions.length > 0 ? 'Start Quiz / Learn' : 'Start Learning'}
                    </Button>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <Button className="w-full" onClick={enrollInCourse}>
                      <BookOpen className="h-4 w-4 mr-2" />
                      Enroll in Course
                    </Button>
                    <p className="text-xs text-center text-muted-foreground">
                      Enroll to track your progress
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Course Info */}
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Course Info</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Status</span>
                  <span className="capitalize">{course.status}</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Type</span>
                  <span className="capitalize">{course.course_type}</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Created</span>
                  <span>{new Date(course.created_at).toLocaleDateString()}</span>
                </div>
                {questions.length > 0 && (
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">Quiz</span>
                    <span>{questions.length} questions</span>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  )
}
