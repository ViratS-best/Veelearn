import { Navigate } from 'react-router-dom'
import { useAuth } from '@/context/AuthContext'

export default function RegisterPage() {
  const { token } = useAuth()
  
  if (token) {
    return <Navigate to="/dashboard" replace />
  }
  
  // Registration is handled in LoginPage via tabs
  return <Navigate to="/login" replace />
}
