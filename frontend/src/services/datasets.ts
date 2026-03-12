import { api } from './api'
import type { Dataset } from '@/types'

export const datasetsService = {
  async upload(file: File, description: string): Promise<Dataset> {
    const form = new FormData()
    form.append('file', file)
    form.append('description', description)
    const res = await api.post<Dataset>('/datasets/upload', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return res.data
  },
  async list(): Promise<Dataset[]> {
    const res = await api.get<Dataset[]>('/datasets/')
    return res.data
  },
  async delete(id: number): Promise<void> {
    await api.delete(`/datasets/${id}`)
  },
}
