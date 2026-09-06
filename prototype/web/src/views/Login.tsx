import { AlertCircle, ChevronDown, Lock, Train, User as UserIcon } from 'lucide-react'
import { useState } from 'react'
import { api } from '../api'
import type { Session } from '../types'

const DEMO_ACCOUNTS = [
  { user: 'p.way.jaipur', label: 'Engineering (P.Way)' },
  { user: 'snt.jaipur', label: 'Signalling & Telecom' },
  { user: 'ohe.jaipur', label: 'Traction (OHE)' },
  { user: 'controller', label: 'Section controller' },
]

export function Login({ onLoggedIn }: { onLoggedIn: (s: Session) => void }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [hintsOpen, setHintsOpen] = useState(false)

  async function submit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const session = await api.login(username.trim(), password)
      onLoggedIn(session)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex h-screen items-center justify-center bg-[var(--bg)] px-4">
      <div className="w-full max-w-sm">
        <div className="mb-8 flex flex-col items-center text-center">
          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[var(--navy)] text-white">
            <Train size={22} />
          </div>
          <h1 className="mt-3 text-xl font-extrabold text-[var(--ink)]">RailBlock</h1>
          <p className="mt-1 text-sm text-[var(--ink-soft)]">Sign in to plan the corridor.</p>
        </div>

        <form onSubmit={submit} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <label className="flex flex-col gap-1.5 text-xs font-semibold text-[var(--ink-soft)]">
            Username
            <div className="flex items-center gap-2 rounded-lg border border-slate-300 px-3 py-2 focus-within:border-[var(--navy)]">
              <UserIcon size={15} className="text-[var(--ink-faint)]" />
              <input
                value={username} onChange={(e) => setUsername(e.target.value)}
                autoFocus autoComplete="username"
                className="w-full text-sm font-normal text-[var(--ink)] outline-none"
                placeholder="e.g. p.way.jaipur"
              />
            </div>
          </label>

          <label className="mt-4 flex flex-col gap-1.5 text-xs font-semibold text-[var(--ink-soft)]">
            Password
            <div className="flex items-center gap-2 rounded-lg border border-slate-300 px-3 py-2 focus-within:border-[var(--navy)]">
              <Lock size={15} className="text-[var(--ink-faint)]" />
              <input
                type="password" value={password} onChange={(e) => setPassword(e.target.value)}
                autoComplete="current-password"
                className="w-full text-sm font-normal text-[var(--ink)] outline-none"
                placeholder="••••••••"
              />
            </div>
          </label>

          {error && (
            <div className="mt-4 flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-800">
              <AlertCircle size={15} className="flex-none" /> {error}
            </div>
          )}

          <button
            type="submit" disabled={loading || !username || !password}
            className="mt-5 w-full rounded-lg bg-[var(--navy)] py-2.5 text-sm font-semibold text-white transition-opacity hover:opacity-90 disabled:opacity-50"
          >
            {loading ? 'Signing in…' : 'Sign in'}
          </button>
        </form>

        <div className="mt-4 rounded-xl border border-slate-200 bg-white">
          <button
            onClick={() => setHintsOpen((v) => !v)}
            className="flex w-full items-center justify-between px-4 py-3 text-xs font-semibold text-[var(--ink-soft)]"
          >
            Demo accounts for this corridor
            <ChevronDown size={14} className={`transition-transform ${hintsOpen ? 'rotate-180' : ''}`} />
          </button>
          {hintsOpen && (
            <div className="border-t border-slate-100 px-4 py-3 text-xs text-[var(--ink-soft)]">
              <p className="mb-2">Password for every account: <code className="mono rounded bg-slate-100 px-1.5 py-0.5">railblock2026</code></p>
              {DEMO_ACCOUNTS.map((a) => (
                <div key={a.user} className="flex justify-between py-0.5">
                  <span className="mono">{a.user}</span>
                  <span>{a.label}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
