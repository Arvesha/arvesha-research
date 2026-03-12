import { api } from './api'
import type { BenchmarkRunRequest, BenchmarkRunResponse } from '@/types'

export const benchmarksService = {
  async run(data: BenchmarkRunRequest): Promise<BenchmarkRunResponse> {
    const res = await api.post<BenchmarkRunResponse>('/benchmark/run', data)
    return res.data
  },
}
