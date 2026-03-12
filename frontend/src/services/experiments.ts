import { api } from './api'
import type { ResearchExperiment, CreateExperimentRequest } from '@/types'

export const experimentsService = {
  async create(data: CreateExperimentRequest): Promise<ResearchExperiment> {
    const res = await api.post<ResearchExperiment>('/research/experiment', data)
    return res.data
  },
  async list(): Promise<ResearchExperiment[]> {
    const res = await api.get<ResearchExperiment[]>('/research/experiments')
    return res.data
  },
  async get(id: number): Promise<ResearchExperiment> {
    const res = await api.get<ResearchExperiment>(`/research/experiment/${id}`)
    return res.data
  },
  async delete(id: number): Promise<void> {
    await api.delete(`/research/experiment/${id}`)
  },
}
