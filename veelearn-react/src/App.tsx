import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import { Loader2 } from 'lucide-react'

// Pages
import LandingPage from './pages/LandingPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import CourseEditorPage from './pages/CourseEditorPage'
import CourseViewPage from './pages/CourseViewPage'
import CoursePlayerPage from './pages/CoursePlayerPage'
import MarketplacePage from './pages/MarketplacePage'
import BlockSimulatorPage from './pages/BlockSimulatorPage'
import VisualSimulatorPage from './pages/VisualSimulatorPage'
import AdminPanelPage from './pages/AdminPanelPage'
import TeacherDashboardPage from './pages/TeacherDashboardPage'
import StudentDashboardPage from './pages/StudentDashboardPage'
import SimulatorViewPage from './pages/SimulatorViewPage'

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, isLoading, token } = useAuth()

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    )
  }

  if (!token || !user) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}

function AdminRoute({ children }: { children: React.ReactNode }) {
  const { user, isLoading } = useAuth()

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    )
  }

  if (!user || (user.role !== 'admin' && user.role !== 'superadmin')) {
    return <Navigate to="/dashboard" replace />
  }

  return <>{children}</>
}

function TeacherRoute({ children }: { children: React.ReactNode }) {
  const { user, isLoading } = useAuth()

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    )
  }

  if (!user || (user.role !== 'teacher' && user.role !== 'admin' && user.role !== 'superadmin')) {
    return <Navigate to="/dashboard" replace />
  }

  return <>{children}</>
}

export default function App() {
  return (
    <Routes>
      {/* Public routes */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      
      {/* Protected routes */}
      <Route path="/dashboard" element={
        <ProtectedRoute>
          <DashboardPage />
        </ProtectedRoute>
      } />
      
      <Route path="/courses/new" element={
        <ProtectedRoute>
          <CourseEditorPage />
        </ProtectedRoute>
      } />
      
      <Route path="/courses/:id/edit" element={
        <ProtectedRoute>
          <CourseEditorPage />
        </ProtectedRoute>
      } />
      
      <Route path="/courses/:id" element={
        <ProtectedRoute>
          <CourseViewPage />
        </ProtectedRoute>
      } />
      
      <Route path="/player/:id" element={
        <ProtectedRoute>
          <CoursePlayerPage />
        </ProtectedRoute>
      } />
      
      <Route path="/marketplace" element={
        <ProtectedRoute>
          <MarketplacePage />
        </ProtectedRoute>
      } />
      
      <Route path="/block-simulator" element={
        <ProtectedRoute>
          <BlockSimulatorPage />
        </ProtectedRoute>
      } />
      
      <Route path="/visual-simulator" element={
        <ProtectedRoute>
          <VisualSimulatorPage />
        </ProtectedRoute>
      } />
      
      <Route path="/simulator/:id" element={
        <ProtectedRoute>
          <SimulatorViewPage />
        </ProtectedRoute>
      } />
      
      <Route path="/admin" element={
        <AdminRoute>
          <AdminPanelPage />
        </AdminRoute>
      } />
      
      <Route path="/teacher" element={
        <TeacherRoute>
          <TeacherDashboardPage />
        </TeacherRoute>
      } />
      
      <Route path="/student" element={
        <ProtectedRoute>
          <StudentDashboardPage />
        </ProtectedRoute>
      } />
      
      {/* Public landing page */}
      <Route path="/" element={<LandingPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
