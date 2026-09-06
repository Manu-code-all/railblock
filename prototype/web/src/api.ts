import type {
  ActivityRow,
  Explanation,
  Meta,
  RequestRow,
  SolveResult,
  WindowRow,
} from './types'

const BASE = '/api'

async function req<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  })
  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(body.detail || `Request failed: ${res.status}`)
  }
  return res.json()
}

export const api = {
  meta: () => req<Meta>('/meta'),

  windows: () => req<WindowRow[]>('/windows'),

  requests: (dept?: string, status?: string) => {
    const qs = new URLSearchParams()
    if (dept) qs.set('dept', dept)
    if (status) qs.set('status', status)
    const suffix = qs.toString() ? `?${qs}` : ''
    return req<RequestRow[]>(`/requests${suffix}`)
  },

  submit: (body: {
    dept: string
    section: string
    title: string
    duration: number
    priority: number
    deadline_day: number
    actor: string
  }) => req<{ id: string; warning: string | null }>('/requests', {
    method: 'POST',
    body: JSON.stringify(body),
  }),

  withdraw: (rid: string, actor: string) =>
    req<{ ok: true }>(`/requests/${rid}?actor=${encodeURIComponent(actor)}`, {
      method: 'DELETE',
    }),

  defer: (rid: string, actor: string) =>
    req<{ ok: true }>(`/requests/${rid}/defer?actor=${encodeURIComponent(actor)}`, {
      method: 'POST',
    }),

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

  createPlan: (strict: boolean, urgency: number, actor: string) =>
    req<{ id: number }>(`/plans?actor=${encodeURIComponent(actor)}`, {
      method: 'POST',
      body: JSON.stringify({ strict, urgency }),
    }),

  publish: (pid: number, actor: string) =>
    req<{ ok: true }>(`/plans/${pid}/publish`, {
      method: 'POST',
      body: JSON.stringify({ actor }),
    }),

  published: () => req<{ plan: any; blocks: any[] }>('/plans/published'),

  activity: (limit = 200) => req<ActivityRow[]>(`/activity?limit=${limit}`),

  exportCsvUrl: () => `${BASE}/export/csv`,
}
