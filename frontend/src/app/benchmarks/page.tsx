'use client'

import { useState } from 'react'
import { MainLayout } from '@/components/layout/main-layout'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Spinner } from '@/components/ui/spinner'
import { benchmarksService } from '@/services/benchmarks'
import type { BenchmarkRunResponse } from '@/types'
import toast from 'react-hot-toast'

export default function BenchmarksPage() {
  const [models, setModels] = useState('gpt-4o-mini\ngpt-3.5-turbo')
  const [prompts, setPrompts] = useState('What is the capital of France?\nExplain quantum computing in simple terms.')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<BenchmarkRunResponse | null>(null)

  const handleRun = async () => {
    const modelList = models.split('\n').map((m) => m.trim()).filter(Boolean)
    const promptList = prompts.split('\n').map((p) => p.trim()).filter(Boolean)
    if (!modelList.length || !promptList.length) { toast.error('Add at least one model and prompt'); return }
    setLoading(true)
    try {
      const res = await benchmarksService.run({ name: 'Benchmark', models: modelList, prompts: promptList, metrics: ['latency', 'tokens', 'cost'] })
      setResult(res)
      toast.success('Benchmark complete!')
    } catch {
      toast.error('Benchmark failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <MainLayout>
      <div className="space-y-6">
        <h1 className="text-2xl font-bold">Benchmarks 📈</h1>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader><CardTitle>Configuration</CardTitle></CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Models (one per line)</label>
                <textarea className="w-full px-3 py-2 rounded-lg bg-input border border-border focus:outline-none focus:ring-2 focus:ring-ring h-28 resize-none font-mono text-sm" value={models} onChange={(e) => setModels(e.target.value)} />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Prompts (one per line)</label>
                <textarea className="w-full px-3 py-2 rounded-lg bg-input border border-border focus:outline-none focus:ring-2 focus:ring-ring h-28 resize-none text-sm" value={prompts} onChange={(e) => setPrompts(e.target.value)} />
              </div>
              <Button onClick={handleRun} disabled={loading} className="w-full">
                {loading ? <><Spinner className="h-4 w-4 mr-2" />Running Benchmark...</> : '▶ Run Benchmark'}
              </Button>
            </CardContent>
          </Card>
          <div>
            {loading && <div className="flex flex-col items-center justify-center h-full gap-3"><Spinner /><p className="text-muted-foreground">Running benchmarks...</p></div>}
            {!loading && !result && (
              <Card className="h-full flex items-center justify-center">
                <CardContent className="text-center text-muted-foreground py-12">Configure and run a benchmark to see results</CardContent>
              </Card>
            )}
          </div>
        </div>

        {result && (
          <Card>
            <CardHeader><CardTitle>Results — {result.name}</CardTitle></CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-border">
                      {['Model', 'Prompt', 'Latency', 'Tokens', 'Cost', 'Response'].map((h) => (
                        <th key={h} className="text-left py-2 px-3 text-muted-foreground font-medium">{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {result.results.map((r, i) => (
                      <tr key={i} className="border-b border-border/50 hover:bg-accent/30">
                        <td className="py-2 px-3"><Badge variant="secondary">{r.model}</Badge></td>
                        <td className="py-2 px-3 max-w-xs truncate text-muted-foreground">{r.prompt}</td>
                        <td className="py-2 px-3">{r.latency_ms.toFixed(0)}ms</td>
                        <td className="py-2 px-3">{r.tokens_used}</td>
                        <td className="py-2 px-3">${r.cost_estimate.toFixed(5)}</td>
                        <td className="py-2 px-3 max-w-xs truncate text-muted-foreground">{r.response}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </MainLayout>
  )
}
