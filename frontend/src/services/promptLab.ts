import { api } from './api'
import type { PromptTestRequest, PromptTestResponse } from '@/types'

export const promptLabService = {
  async test(data: PromptTestRequest): Promise<PromptTestResponse> {
    const res = await api.post<PromptTestResponse>('/research/test-prompt', data)
    return res.data
  },
}
