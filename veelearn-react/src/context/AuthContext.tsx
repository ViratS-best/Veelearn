import { createContext, useContext, useState, useEffect, ReactNode } from 'react'

// API Base URL - supports both local, GitHub Pages, and Custom Domain
const getApiBaseUrl = () => {
  const hostname = window.location.hostname;
  if (hostname.includes('veelearn.org')) {
    return 'https://api.veelearn.org';
  }
  if (hostname.includes('github.io') || hostname.includes('onrender.com')) {
    return 'https://veelearn-backend.onrender.com';
  }
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return 'http://localhost:3000';
  }
  return window.location.origin;
}

export const API_BASE_URL = getApiBaseUrl()

interface User {
  id: number
  email: string
  name: string
  role: 'user' | 'teacher' | 'admin' | 'superadmin'
  class_code?: string
  teacher_approved?: boolean
}

interface AuthContextType {
  user: User | null
  token: string | null
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (name: string, email: string, password: string) => Promise<void>
  logout: () => void
  updateUser: (user: User) => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const storedToken = localStorage.getItem('token')
    const storedUser = localStorage.getItem('user')
    
    if (storedToken && storedUser) {
      setToken(storedToken)
      try {
        setUser(JSON.parse(storedUser))
      } catch {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
      }
    }
    setIsLoading(false)
  }, [])

  const login = async (email: string, password: string) => {
    const response = await fetch(`${API_BASE_URL}/api/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
      credentials: 'include',
    })
    
    const data = await response.json()
    
    if (!response.ok) {
      throw new Error(data.message || 'Login failed')
    }
    
    const authToken = data.data?.token || data.token
    if (!authToken) {
      throw new Error('No token received')
    }
    
    localStorage.setItem('token', authToken)
    setToken(authToken)
    
    // Fetch user profile
    const profileResponse = await fetch(`${API_BASE_URL}/api/users/profile`, {
      headers: { Authorization: `Bearer ${authToken}` },
    })
    
    if (profileResponse.ok) {
      const profileData = await profileResponse.json()
      const userData = profileData.data || profileData
      setUser(userData)
      localStorage.setItem('user', JSON.stringify(userData))
    }
  }

  const register = async (name: string, email: string, password: string) => {
    const response = await fetch(`${API_BASE_URL}/api/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password }),
      credentials: 'include',
    })
    
    const data = await response.json()
    
    if (!response.ok) {
      throw new Error(data.message || 'Registration failed')
    }
    
    // Auto-login after registration
    await login(email, password)
  }

  const logout = async () => {
    try {
      if (token) {
        await fetch(`${API_BASE_URL}/api/logout`, {
          method: 'POST',
          headers: { Authorization: `Bearer ${token}` },
          credentials: 'include',
        })
      }
    } catch {
      // Ignore logout errors
    }
    
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setToken(null)
    setUser(null)
  }

  const updateUser = (updatedUser: User) => {
    setUser(updatedUser)
    localStorage.setItem('user', JSON.stringify(updatedUser))
  }

  return (
    <AuthContext.Provider value={{ user, token, isLoading, login, register, logout, updateUser }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
