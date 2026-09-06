export type Dept = 'ENGG' | 'S&T' | 'TRD'

export interface User {
  username: string
  display_name: string
  dept: Dept | null
}

export interface Session extends User {
  token: string
}

export interface Section {
  id: string
  name: string
}

export interface WindowRow {
  id: string
  section: string
  start: number
  end: number
  disruption: number
}

export interface Meta {
  sections: Section[]
  sectionCount: number
  windowCount: number
  days: number
  pendingCount: number
  published: Plan | null
}

export interface RequestRow {
  id: string
  dept: Dept
  section: string
  title: string
  duration: number
  priority: number
  deadline_day: number
  status: 'pending' | 'planned' | 'deferred'
  submitted_by: string
  submitted_at: string
}

export interface Block {
  request: string
  dept: Dept
  section: string
  sectionName: string
  title: string
  start: number
  end: number
  priority: number
  window: string
}

export interface ConflictRequest {
  id: string
  dept: Dept
  section: string
  sectionName: string
  deptName: string
  title: string
  duration: number
  priority: number
  deadline_day: number
}

export interface SolveResult {
  status: string
  ok: boolean
  provenOptimal: boolean
  blocks: Block[]
  unscheduled: ConflictRequest[]
  conflict: ConflictRequest[]
  conflictText: string | null
  solveTimeMs: number
  violations: string[]
  requestCount: number
  days: number
}

export interface WindowVerdict {
  window: string
  day: number
  span: string
  ok: boolean
  why: string
}

export interface Explanation {
  request: string
  scheduled: boolean
  headline: string
  reasons: string[]
  alternatives: WindowVerdict[]
}

export interface Plan {
  id: number
  created_at: string
  created_by: string
  days: number
  urgency: number
  strict: number
  status: 'draft' | 'published'
  solver: string
  solve_ms: number
  conflict: string
}

export interface PublishedBlock {
  plan_id: number
  request_id: string
  dept: Dept
  section: string
  sectionName: string
  deptName: string
  title: string
  start: number
  end: number
  priority: number
  window_id: string
  day: number
}

export interface ActivityRow {
  id: number
  at: string
  actor: string
  action: string
  detail: string
}

export const DEPT_NAME: Record<string, string> = {
  ENGG: 'Engineering (P.Way)',
  'S&T': 'Signalling & Telecom',
  TRD: 'Traction (OHE)',
}

export const DEPT_COLOR: Record<string, string> = {
  ENGG: '#2E6DA4',
  'S&T': '#1E8449',
  TRD: '#B8790A',
}
