'use client'

import { useState } from 'react'
import { MainLayout } from '@/components/layout/main-layout'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Spinner } from '@/components/ui/spinner'
import { agentsService } from '@/services/agents'
import type { AgentRunResponse } from '@/types'
import toast from 'react-hot-toast'

const AGENTS = [
  { value: 'research', label: 'Research Agent', icon: '🔬', desc: 'Multi-step research with tool use' },
  { value: 'summarization', label: 'Summarization Agent', icon: '📝', desc: 'Summarize documents' },
  { value: 'data_extraction', label: 'Data Extraction Agent', icon: '⛏️', desc: 'Extract structured data' },
]

export default function AgentsPage() {
  const [agentType, setAgentType] = useState('research')
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<AgentRunResponse | null>(null)

  const handleRun = async () => {
    if (!input.trim()) { toast.error('Enter an input'); return }
    setLoading(true)
    try {
      const res = await agentsService.run({ agent_type: agentType, input })
      setResult(res)
    } catch {
      toast.error('Agent run failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <MainLayout>
      <div className="space-y-6">
        <h1 className="text-2xl font-bold">Agent Playground 🤖</h1>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-4">
          {AGENTS.map((agent) => (
            <div
              key={agent.value}
              onClick={() => setAgentType(agent.value)}
              className={`p-4 rounded-xl border cursor-pointer transition-colors ${agentType === agent.value ? 'border-primary bg-primary/10' : 'border-border hover:border-primary/50'}`}
            >
              <div className="text-2xl mb-2">{agent.icon}</div>
              <div className="font-medium text-sm">{agent.label}</div>
              <div className="text-xs text-muted-foreground mt-1">{agent.desc}</div>
            </div>
          ))}
        </div>

        <Card>
          <CardContent className="pt-6 space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Input</label>
              <textarea
                className="w-full px-3 py-2 rounded-lg bg-input border border-border focus:outline-none focus:ring-2 focus:ring-ring h-32 resize-none"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Enter your research query or text to process..."
              />
            </div>
            <Button onClick={handleRun} disabled={loading}>
              {loading ? <><Spinner className="h-4 w-4 mr-2" />Running Agent...</> : '▶ Run Agent'}
            </Button>
          </CardContent>
        </Card>

        {result && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                Result <Badge variant="secondary">{result.agent_type}</Badge>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="bg-secondary/50 rounded-lg p-4 text-sm whitespace-pre-wrap">{result.output}</div>
              {result.steps.length > 0 && (
                <div>
                  <p className="text-sm font-medium mb-2">Steps:</p>
                  <div className="space-y-2">
                    {result.steps.map((step) => (
                      <div key={step.step} className="bg-muted/30 rounded p-3 text-xs">
                        <span className="font-medium">Step {step.step} — {step.action}: </span>
                        {step.observation}
                      </div>
                    ))}
                  </div>
                </div>
              )}
              {result.tokens_used > 0 && <p className="text-xs text-muted-foreground">Tokens used: {result.tokens_used}</p>}
            </CardContent>
          </Card>
        )}
      </div>
    </MainLayout>
  )
}
