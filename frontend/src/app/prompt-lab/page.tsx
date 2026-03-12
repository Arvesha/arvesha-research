'use client'

import { useState } from 'react'
import { MainLayout } from '@/components/layout/main-layout'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Spinner } from '@/components/ui/spinner'
import { promptLabService } from '@/services/promptLab'
import type { PromptTestResponse } from '@/types'
import toast from 'react-hot-toast'

const MODELS = ['gpt-4o-mini', 'gpt-4o', 'gpt-3.5-turbo']

export default function PromptLabPage() {
  const [prompt, setPrompt] = useState('')
  const [model, setModel] = useState('gpt-4o-mini')
  const [temperature, setTemperature] = useState(0.7)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<PromptTestResponse | null>(null)

  const handleRun = async () => {
    if (!prompt.trim()) { toast.error('Enter a prompt'); return }
    setLoading(true)
    try {
      const res = await promptLabService.test({ prompt, model, temperature })
      setResult(res)
    } catch {
      toast.error('Prompt test failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <MainLayout>
      <div className="space-y-6">
        <h1 className="text-2xl font-bold">Prompt Lab 🧪</h1>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="space-y-4">
            <Card>
              <CardHeader><CardTitle>Configuration</CardTitle></CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Model</label>
                  <select className="w-full px-3 py-2 rounded-lg bg-input border border-border focus:outline-none focus:ring-2 focus:ring-ring" value={model} onChange={(e) => setModel(e.target.value)}>
                    {MODELS.map((m) => <option key={m} value={m}>{m}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Temperature: {temperature}</label>
                  <input type="range" min={0} max={2} step={0.1} value={temperature} onChange={(e) => setTemperature(Number(e.target.value))} className="w-full" />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Prompt</label>
                  <textarea
                    className="w-full px-3 py-2 rounded-lg bg-input border border-border focus:outline-none focus:ring-2 focus:ring-ring h-40 resize-none font-mono text-sm"
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="Enter your prompt here..."
                  />
                </div>
                <Button onClick={handleRun} disabled={loading} className="w-full">
                  {loading ? <><Spinner className="h-4 w-4 mr-2" />Running...</> : '▶ Run Prompt'}
                </Button>
              </CardContent>
            </Card>
          </div>

          <div>
            <Card className="h-full">
              <CardHeader><CardTitle>Response</CardTitle></CardHeader>
              <CardContent>
                {loading ? (
                  <div className="flex justify-center py-8"><Spinner /></div>
                ) : result ? (
                  <div className="space-y-4">
                    <div className="bg-secondary/50 rounded-lg p-4 font-mono text-sm whitespace-pre-wrap">{result.response}</div>
                    <div className="flex gap-4 text-sm text-muted-foreground">
                      <span>🎯 {result.tokens_used} tokens</span>
                      <span>⏱ {result.latency_ms.toFixed(0)}ms</span>
                    </div>
                  </div>
                ) : (
                  <p className="text-muted-foreground text-center py-8">Run a prompt to see the response</p>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </MainLayout>
  )
}
