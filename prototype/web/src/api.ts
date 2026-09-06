import type {
  ActivityRow,
  Explanation,
  Meta,
  RequestRow,
  Session,
  SolveResult,
  WindowRow,
} from './types'

const BASE = '/api'
const TOKEN_KEY = 'railblock.token'

let token: string | null = localStorage.getItem(TOKEN_KEY)

function setToken(t: string | null) {
  token = t
  if (t) localStorage.setItem(TOKEN_KEY, t)
  else localStorage.removeItem(TOKEN_KEY)
}

async function req<T>(path: string, init?: RequestInit): Promise<T> {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' }
  if (token) headers.Authorization = `Bearer ${token}`
  const res = await fetch(`${BASE}${path}`, { headers, ...init })
  if (res.status === 401) {
    setToken(null)
    throw new Error('Session expired — please log in again.')
  }
  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(body.detail || `Request failed: ${res.status}`)
  }
  return res.json()
}

export const api = {
  isLoggedIn: () => token !== null,

  login: async (username: string, password: string) => {
    const session = await req<Session>('/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    })
    setToken(session.token)
    return session
  },

  logout: async () => {
    await req('/logout', { method: 'POST' }).catch(() => {})
    setToken(null)
  },

  me: () => req<Session>('/me'),

  meta: () => req<Meta>('/meta'),

  windows: () => req<WindowRow[]>('/windows'),

  requests: (status?: string) => {
    const suffix = status ? `?status=${status}` : ''
    return req<RequestRow[]>(`/requests${suffix}`)
  },

  submit: (body: {
    section: string
    title: string
    duration: number
    priority: number
    deadline_day: number
  }) => req<{ id: string; warning: string | null }>('/requests', {
    method: 'POST',
    body: JSON.stringify(body),
  }),

  withdraw: (rid: string) =>
    req<{ ok: true }>(`/requests/${rid}`, { method: 'DELETE' }),

  defer: (rid: string) =>
    req<{ ok: true }>(`/requests/${rid}/defer`, { method: 'POST' }),

  solve: (strict: boolean, urgency: number) =>
    req<SolveResult>('/solve', {
      method: 'POST',
      body: JSON.stringify({ strict, urgency }),
    }),

  explain: (rid: string, strict: boolean, urgency: number) =>
    req<Explanation>('/explain', {
      method: 'POST',
      body: JSON.stringify({ rid, strict, urgency }),
    }),

  createPlan: (strict: boolean, urgency: number) =>
    req<{ id: number }>('/plans', {
      method: 'POST',
      body: JSON.stringify({ strict, urgency }),
    }),

  publish: (pid: number) =>
    req<{ ok: true }>(`/plans/${pid}/publish`, { method: 'POST' }),

  published: () => req<{ plan: any; blocks: any[] }>('/plans/published'),

  activity: (limit = 200) => req<ActivityRow[]>(`/activity?limit=${limit}`),

  exportCsv: async () => {
    const res = await fetch(`${BASE}/export/csv`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    })
    if (!res.ok) throw new Error('No block order published yet.')
    const blob = await res.blob()
    const filename = res.headers.get('Content-Disposition')?.match(/filename=(.+)/)?.[1]
      ?? 'block_order.csv'
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.click()
    URL.revokeObjectURL(url)
  },
}
