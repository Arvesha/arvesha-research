import { api } from './api'
import type { AuthTokens, LoginRequest, RegisterRequest, User } from '@/types'

export const authService = {
  async login(data: LoginRequest): Promise<AuthTokens> {
    const res = await api.post<AuthTokens>('/auth/login', data)
    return res.data
  },
  async register(data: RegisterRequest): Promise<User> {
    const res = await api.post<User>('/auth/register', data)
    return res.data
  },
  async me(): Promise<User> {
    const res = await api.get<User>('/auth/me')
    return res.data
  },
}
