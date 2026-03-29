import { useState, useEffect } from 'react'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogFooter
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { Label } from '@/components/ui/label'

declare global {
  interface Window {
    MathJax: any;
  }
}

interface LatexEditorModalProps {
  isOpen: boolean
  onClose: () => void
  onInsert: (latexHtml: string) => void
}

const symbols = [
  { label: 'α', value: '\\alpha' },
  { label: 'β', value: '\\beta' },
  { label: 'γ', value: '\\gamma' },
  { label: 'Δ', value: '\\Delta' },
  { label: 'a/b', value: '\\frac{a}{b}' },
  { label: '√x', value: '\\sqrt{x}' },
  { label: 'x²', value: 'x^2' },
  { label: 'xᵢ', value: 'x_i' },
  { label: 'Σ', value: '\\sum' },
  { label: '∫', value: '\\int' },
  { label: '±', value: '\\pm' },
  { label: '×', value: '\\times' }
]

const templates = [
  { label: 'E = mc²', value: 'E = mc^2' },
  { label: 'Quadratic Formula', value: 'x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}' },
  { label: 'Limit', value: '\\lim_{x \\to \\infty} f(x)' },
  { label: 'Integral', value: '\\int_{a}^{b} x^2 dx' }
]

export default function LatexEditorModal({ isOpen, onClose, onInsert }: LatexEditorModalProps) {
  const [equation, setEquation] = useState('')
  const [mode, setMode] = useState<'inline' | 'display'>('inline')

  const formattedEquation = mode === 'inline' ? `$${equation}$` : `$$${equation}$$`

  useEffect(() => {
    if (isOpen && window.MathJax) {
      setTimeout(() => {
        window.MathJax.typesetPromise?.()
      }, 100)
    }
  }, [isOpen, equation, mode])

  const insertSymbol = (val: string) => setEquation((prev) => prev + val)

  const handleInsert = () => {
    if (!equation.trim()) return
    const html = `<span class="latex-equation" data-mode="${mode}">${formattedEquation}</span>`
    onInsert(html)
    setEquation('')
    onClose()
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-3xl">
        <DialogHeader>
          <DialogTitle>Insert LaTeX Equation</DialogTitle>
          <DialogDescription>
            Type LaTeX code or use the buttons below to build your math equation.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4 py-4">
          <div className="flex gap-4 items-center">
            <RadioGroup defaultValue="inline" value={mode} onValueChange={(v) => setMode(v as 'inline'|'display')} className="flex gap-4">
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="inline" id="r1" />
                <Label htmlFor="r1">Inline ($...$)</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="display" id="r2" />
                <Label htmlFor="r2">Display ($$...$$)</Label>
              </div>
            </RadioGroup>
          </div>

          <div className="grid grid-cols-6 gap-2 sm:grid-cols-12">
            {symbols.map((sym, i) => (
              <Button key={i} variant="outline" size="sm" onClick={() => insertSymbol(sym.value)} title={sym.value}>
                {sym.label}
              </Button>
            ))}
          </div>
          
          <div className="flex flex-wrap gap-2">
            {templates.map((tpl, i) => (
              <Button key={i} variant="secondary" size="sm" onClick={() => setEquation(tpl.value)}>
                {tpl.label}
              </Button>
            ))}
          </div>

          <Textarea 
            value={equation} 
            onChange={(e) => setEquation(e.target.value)}
            placeholder="e.g. \frac{a}{b}"
            className="font-mono"
            rows={4}
          />

          <div className="mt-4 p-4 border rounded bg-muted min-h-[80px] flex items-center justify-center text-lg overflow-x-auto">
            {equation.trim() ? (
              <div id="latex-live-preview">{formattedEquation}</div>
            ) : (
              <span className="text-muted-foreground italic text-sm">Preview will appear here</span>
            )}
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleInsert}>Insert Equation</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
