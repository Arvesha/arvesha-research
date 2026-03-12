import { api } from './api'
import type { RAGQueryRequest, RAGQueryResponse } from '@/types'

export const ragService = {
  async query(data: RAGQueryRequest): Promise<RAGQueryResponse> {
    const res = await api.post<RAGQueryResponse>('/rag/query', data)
    return res.data
  },
}
