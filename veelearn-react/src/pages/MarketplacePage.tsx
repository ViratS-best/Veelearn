import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth, API_BASE_URL } from '@/context/AuthContext'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { toast } from 'sonner'
import {
  Search,
  Plus,
  Star,
  Download,
  Eye,
  Filter,
  Grid,
  List,
  Blocks,
  Code,
  Trash2,
  Edit,
  ExternalLink
} from 'lucide-react'

interface Simulator {
  id: number
  name: string
  description: string
  category: string
  is_public: number
  downloads: number
  rating?: number
  creator_id: number
  creator_email?: string
  created_at: string
}

export default function MarketplacePage() {
  const navigate = useNavigate()
  const { token, user } = useAuth()
  const [simulators, setSimulators] = useState<Simulator[]>([])
  const [mySimulators, setMySimulators] = useState<Simulator[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [category, setCategory] = useState('all')

  useEffect(() => {
    if (token) {
      loadSimulators()
    }
  }, [token])

  const loadSimulators = async () => {
    try {
      const headers = { Authorization: `Bearer ${token}` }
      
      // Load all public simulators
      const res = await fetch(`${API_BASE_URL}/api/simulators`, { headers })
      const data = await res.json()
      if (data.success) {
        setSimulators(data.data || [])
      }

      // Load user's simulators
      const myRes = await fetch(`${API_BASE_URL}/api/my-simulators`, { headers })
      const myData = await myRes.json()
      if (myData.success) {
        setMySimulators(myData.data || [])
      }
    } catch (error) {
      toast.error('Failed to load simulators')
    } finally {
      setIsLoading(false)
    }
  }

  const deleteSimulator = async (id: number) => {
    if (!confirm('Are you sure you want to delete this simulator?')) return

    try {
      const response = await fetch(`${API_BASE_URL}/api/simulators/${id}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` },
      })
      const data = await response.json()
      
      if (data.success) {
        toast.success('Simulator deleted')
        loadSimulators()
      } else {
        toast.error(data.message || 'Failed to delete')
      }
    } catch (error) {
      toast.error('Failed to delete simulator')
    }
  }

  const filteredSimulators = simulators.filter(sim => {
    const matchesSearch = sim.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      sim.description?.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesCategory = category === 'all' || sim.category === category
    return matchesSearch && matchesCategory
  })

  const openSimulator = (id: number) => {
    navigate(`/simulator/${id}`)
  }

  const getCategoryIcon = (cat: string) => {
    switch (cat) {
      case 'block':
        return <Blocks className="h-4 w-4" />
      case 'visual':
        return <Code className="h-4 w-4" />
      default:
        return <Blocks className="h-4 w-4" />
    }
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-surface">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-heading font-bold">Simulator Marketplace</h1>
              <p className="text-muted-foreground">Discover and share interactive simulations</p>
            </div>
            <div className="flex gap-2">
              <Button onClick={() => navigate('/block-simulator')}>
                <Plus className="h-4 w-4 mr-2" />
                Create Block Sim
              </Button>
              <Button variant="outline" onClick={() => navigate('/visual-simulator')}>
                <Plus className="h-4 w-4 mr-2" />
                Create Visual Sim
              </Button>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        {/* Search and Filters */}
        <div className="flex flex-col md:flex-row gap-4 mb-8">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search simulators..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9"
            />
          </div>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="px-4 py-2 rounded-md border border-input bg-background"
          >
            <option value="all">All Categories</option>
            <option value="block">Block-Based</option>
            <option value="visual">Visual/Code</option>
            <option value="physics">Physics</option>
            <option value="math">Math</option>
          </select>
        </div>

        <Tabs defaultValue="browse" className="space-y-6">
          <TabsList>
            <TabsTrigger value="browse">Browse ({filteredSimulators.length})</TabsTrigger>
            <TabsTrigger value="my-simulators">My Simulators ({mySimulators.length})</TabsTrigger>
          </TabsList>

          <TabsContent value="browse">
            {isLoading ? (
              <div className="text-center py-12 text-muted-foreground">Loading simulators...</div>
            ) : filteredSimulators.length === 0 ? (
              <div className="text-center py-12">
                <Blocks className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p className="text-muted-foreground">No simulators found</p>
                <Button className="mt-4" onClick={() => navigate('/block-simulator')}>
                  Create First Simulator
                </Button>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredSimulators.map((sim) => (
                  <Card key={sim.id} className="hover:bg-accent/5 transition-colors">
                    <CardHeader>
                      <div className="flex items-start justify-between">
                        <div className="flex items-center gap-2">
                          {getCategoryIcon(sim.category)}
                          <CardTitle className="text-lg">{sim.name}</CardTitle>
                        </div>
                        {sim.rating && (
                          <div className="flex items-center gap-1 text-yellow-500">
                            <Star className="h-4 w-4 fill-current" />
                            <span className="text-sm">{sim.rating.toFixed(1)}</span>
                          </div>
                        )}
                      </div>
                      <CardDescription className="line-clamp-2">
                        {sim.description || 'No description'}
                      </CardDescription>
                    </CardHeader>
                    <CardFooter>
                      <div className="flex items-center justify-between w-full">
                        <div className="flex items-center gap-4 text-sm text-muted-foreground">
                          <span className="flex items-center gap-1">
                            <Download className="h-3 w-3" />
                            {sim.downloads || 0}
                          </span>
                          <span>{sim.creator_email}</span>
                        </div>
                        <div className="flex gap-2">
                          <Button variant="ghost" size="sm" onClick={() => openSimulator(sim.id)}>
                            <Eye className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    </CardFooter>
                  </Card>
                ))}
              </div>
            )}
          </TabsContent>

          <TabsContent value="my-simulators">
            {mySimulators.length === 0 ? (
              <div className="text-center py-12">
                <Blocks className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p className="text-muted-foreground">You haven't created any simulators yet</p>
                <Button className="mt-4" onClick={() => navigate('/block-simulator')}>
                  Create Your First Simulator
                </Button>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {mySimulators.map((sim) => (
                  <Card key={sim.id}>
                    <CardHeader>
                      <div className="flex items-start justify-between">
                        <div className="flex items-center gap-2">
                          {getCategoryIcon(sim.category)}
                          <CardTitle className="text-lg">{sim.name}</CardTitle>
                        </div>
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          sim.is_public ? 'bg-green-600/20 text-green-400' : 'bg-gray-600/20 text-gray-400'
                        }`}>
                          {sim.is_public ? 'Published' : 'Draft'}
                        </span>
                      </div>
                      <CardDescription className="line-clamp-2">
                        {sim.description || 'No description'}
                      </CardDescription>
                    </CardHeader>
                    <CardFooter>
                      <div className="flex gap-2 w-full">
                        <Button variant="outline" size="sm" className="flex-1" onClick={() => openSimulator(sim.id)}>
                          <Eye className="h-4 w-4 mr-1" />
                          View
                        </Button>
                        <Button variant="outline" size="sm" onClick={() => navigate(`/simulator/${sim.id}/edit`)}>
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button variant="outline" size="sm" onClick={() => deleteSimulator(sim.id)}>
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </CardFooter>
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
