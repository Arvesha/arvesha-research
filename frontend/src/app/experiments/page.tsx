'use client'

import { useState } from 'react'
import useSWR from 'swr'
import { MainLayout } from '@/components/layout/main-layout'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Spinner } from '@/components/ui/spinner'
import { experimentsService } from '@/services/experiments'
import type { ResearchExperiment, CreateExperimentRequest } from '@/types'
import toast from 'react-hot-toast'

const DEFAULT_MODELS = ['gpt-4o-mini', 'gpt-4o', 'gpt-3.5-turbo', 'claude-3-haiku']

function NewExperimentModal({ onClose, onCreated }: { onClose: () => void; onCreated: () => void }) {
  const [form, setForm] = useState<CreateExperimentRequest>({ title: '', model: 'gpt-4o-mini' })
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      await experimentsService.create(form)
      toast.success('Experiment created!')
      onCreated()
      onClose()
    } catch {
      toast.error('Failed to create experiment')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-card border border-border rounded-xl w-full max-w-lg p-6">
        <h2 className="text-xl font-semibold mb-4">New Experiment</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Title *</label>
            <input className="w-full px-3 py-2 rounded-lg bg-input border border-border focus:outline-none focus:ring-2 focus:ring-ring" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Description</label>
            <textarea className="w-full px-3 py-2 rounded-lg bg-input border border-border focus:outline-none focus:ring-2 focus:ring-ring h-20 resize-none" value={form.description || ''} onChange={(e) => setForm({ ...form, description: e.target.value })} />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Model *</label>
            <select className="w-full px-3 py-2 rounded-lg bg-input border border-border focus:outline-none focus:ring-2 focus:ring-ring" value={form.model} onChange={(e) => setForm({ ...form, model: e.target.value })}>
              {DEFAULT_MODELS.map((m) => <option key={m} value={m}>{m}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Prompt Template</label>
            <textarea className="w-full px-3 py-2 rounded-lg bg-input border border-border focus:outline-none focus:ring-2 focus:ring-ring h-20 resize-none font-mono text-sm" value={form.prompt_template || ''} onChange={(e) => setForm({ ...form, prompt_template: e.target.value })} placeholder="You are a helpful assistant..." />
          </div>
          <div className="flex gap-2 pt-2">
            <Button type="submit" disabled={loading} className="flex-1">{loading ? 'Creating...' : 'Create Experiment'}</Button>
            <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default function ExperimentsPage() {
  const [showModal, setShowModal] = useState(false)
  const { data: experiments, isLoading, mutate } = useSWR<ResearchExperiment[]>('experiments', experimentsService.list)

  const handleDelete = async (id: number) => {
    try {
      await experimentsService.delete(id)
      toast.success('Deleted')
      mutate()
    } catch {
      toast.error('Failed to delete')
    }
  }

  return (
    <MainLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold">Experiments</h1>
          <Button onClick={() => setShowModal(true)}>+ New Experiment</Button>
        </div>

        {isLoading ? (
          <div className="flex justify-center py-12"><Spinner /></div>
        ) : experiments?.length === 0 ? (
          <Card>
            <CardContent className="py-12 text-center text-muted-foreground">
              No experiments yet. Create your first one!
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-4">
            {experiments?.map((exp) => (
              <Card key={exp.id}>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle>{exp.title}</CardTitle>
                      {exp.description && <p className="text-sm text-muted-foreground mt-1">{exp.description}</p>}
                    </div>
                    <Button variant="destructive" size="sm" onClick={() => handleDelete(exp.id)}>Delete</Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex gap-2 flex-wrap">
                    <Badge variant="secondary">{exp.model}</Badge>
                    {exp.dataset && <Badge variant="outline">{exp.dataset}</Badge>}
                    <Badge variant="outline">{new Date(exp.created_at).toLocaleDateString()}</Badge>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>

      {showModal && <NewExperimentModal onClose={() => setShowModal(false)} onCreated={() => mutate()} />}
    </MainLayout>
  )
}
