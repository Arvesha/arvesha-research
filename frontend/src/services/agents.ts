import { api } from './api'
import type { AgentRunRequest, AgentRunResponse } from '@/types'

export const agentsService = {
  async run(data: AgentRunRequest): Promise<AgentRunResponse> {
    const res = await api.post<AgentRunResponse>('/agents/run', data)
    return res.data
  },
}
