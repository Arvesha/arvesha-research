export interface User {
  id: number
  username: string
  email: string
  is_active: boolean
}

export interface AuthTokens {
  access_token: string
  token_type: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
}

export interface ResearchExperiment {
  id: number
  title: string
  description?: string
  dataset?: string
  model: string
  prompt_template?: string
  created_at: string
  user_id: number
}

export interface CreateExperimentRequest {
  title: string
  description?: string
  dataset?: string
  model: string
  prompt_template?: string
}

export interface Dataset {
  id: number
  name: string
  description?: string
  file_type: string
  chunks_count: number
  created_at: string
  user_id: number
}

export interface Source {
  content: string
  document_id?: string
  score: number
  metadata: Record<string, unknown>
}

export interface RAGQueryRequest {
  query: string
  dataset_id?: number
  top_k?: number
  use_rerank?: boolean
  stream?: boolean
}

export interface RAGQueryResponse {
  answer: string
  sources: Source[]
  tokens_used: number
  latency_ms: number
}

export interface AgentRunRequest {
  agent_type: string
  input: string
  tools?: string[]
}

export interface AgentStep {
  step: number
  action: string
  observation: string
}

export interface AgentRunResponse {
  output: string
  steps: AgentStep[]
  tokens_used: number
  agent_type: string
}

export interface PromptTestRequest {
  prompt: string
  model: string
  temperature: number
}

export interface PromptTestResponse {
  response: string
  tokens_used: number
  latency_ms: number
}

export interface BenchmarkRunRequest {
  name: string
  models: string[]
  prompts: string[]
  metrics: string[]
}

export interface BenchmarkResult {
  model: string
  prompt: string
  response: string
  latency_ms: number
  tokens_used: number
  cost_estimate: number
}

export interface BenchmarkRunResponse {
  id: number
  name: string
  results: BenchmarkResult[]
  created_at: string
}
