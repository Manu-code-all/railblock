import { AlertCircle, ChevronDown, Eye, EyeOff, Lock, Train, User as UserIcon } from 'lucide-react'
import { useState } from 'react'
import { api } from '../api'
import type { Session } from '../types'

const DEMO_ACCOUNTS = [
  { user: 'p.way.jaipur', label: 'Engineering (P.Way)' },
  { user: 'snt.jaipur', label: 'Signalling & Telecom' },
  { user: 'ohe.jaipur', label: 'Traction (OHE)' },
  { user: 'controller', label: 'Section controller' },
]

function SSOButton({ label, glyph }: { label: string; glyph: React.ReactNode }) {
  const [note, setNote] = useState(false)
  return (
    <div className="relative flex-1">
      <button
        type="button"
        onClick={() => setNote(true)}
        onBlur={() => setTimeout(() => setNote(false), 150)}
        className="flex w-full items-center justify-center gap-2 rounded-lg border border-[var(--color-border-strong)] bg-white py-2.5 text-sm font-medium text-[var(--color-text-primary)] transition-colors hover:bg-[var(--color-surface)]"
      >
        {glyph} {label}
      </button>
      {note && (
        <div className="absolute left-0 right-0 top-full z-10 mt-1.5 rounded-md bg-[var(--color-primary)] px-2.5 py-1.5 text-center text-[11px] text-white shadow-[var(--shadow-md)]">
          Not wired up in this demo — use the form below.
        </div>
      )}
    </div>
  )
}

export function Login({ onLoggedIn }: { onLoggedIn: (s: Session) => void }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [remember, setRemember] = useState(true)
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
    <div className="flex h-screen">
      {/* Left — auth panel */}
      <div className="flex w-full flex-col justify-center px-10 py-10 sm:px-16 lg:w-2/5">
        <div className="mx-auto w-full max-w-sm">
          <div className="mb-8 flex items-center gap-2.5">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-[var(--color-primary)] text-white">
              <Train size={20} />
            </div>
            <span className="text-lg font-semibold text-[var(--color-text-primary)]">RailBlock</span>
          </div>

          <h1 className="text-[28px] font-semibold text-[var(--color-text-primary)]">Welcome back</h1>
          <p className="mt-1 text-sm text-[var(--color-text-secondary)]">Sign in to manage rail corridors.</p>

          <div className="mt-6 flex gap-3">
            <SSOButton label="Google" glyph={<GoogleGlyph />} />
            <SSOButton label="Microsoft" glyph={<MicrosoftGlyph />} />
          </div>

          <div className="my-6 flex items-center gap-3 text-xs text-[var(--color-text-muted)]">
            <div className="h-px flex-1 bg-[var(--color-border)]" /> or <div className="h-px flex-1 bg-[var(--color-border)]" />
          </div>

          <form onSubmit={submit}>
            <label className="flex flex-col gap-1.5 text-xs font-medium text-[var(--color-text-secondary)]">
              Username
              <div className="flex items-center gap-2 rounded-lg border border-[var(--color-border-strong)] px-3 py-2.5 focus-within:border-[var(--color-accent)] focus-within:ring-2 focus-within:ring-[var(--color-accent)]/20">
                <UserIcon size={15} className="text-[var(--color-text-muted)]" />
                <input
                  value={username} onChange={(e) => setUsername(e.target.value)}
                  autoFocus autoComplete="username"
                  className="w-full text-sm text-[var(--color-text-primary)] outline-none placeholder:text-[var(--color-text-muted)]"
                  placeholder="e.g. p.way.jaipur"
                />
              </div>
            </label>

            <label className="mt-4 flex flex-col gap-1.5 text-xs font-medium text-[var(--color-text-secondary)]">
              Password
              <div className="flex items-center gap-2 rounded-lg border border-[var(--color-border-strong)] px-3 py-2.5 focus-within:border-[var(--color-accent)] focus-within:ring-2 focus-within:ring-[var(--color-accent)]/20">
                <Lock size={15} className="text-[var(--color-text-muted)]" />
                <input
                  type={showPassword ? 'text' : 'password'} value={password} onChange={(e) => setPassword(e.target.value)}
                  autoComplete="current-password"
                  className="w-full text-sm text-[var(--color-text-primary)] outline-none placeholder:text-[var(--color-text-muted)]"
                  placeholder="••••••••"
                />
                <button type="button" onClick={() => setShowPassword((v) => !v)} aria-label={showPassword ? 'Hide password' : 'Show password'} className="text-[var(--color-text-muted)]">
                  {showPassword ? <EyeOff size={15} /> : <Eye size={15} />}
                </button>
              </div>
            </label>

            <div className="mt-3 flex items-center justify-between text-xs">
              <label className="flex items-center gap-1.5 text-[var(--color-text-secondary)]">
                <input type="checkbox" checked={remember} onChange={(e) => setRemember(e.target.checked)} className="accent-[var(--color-accent)]" />
                Remember me
              </label>
              <button type="button" className="font-medium text-[var(--color-accent)] hover:underline">Forgot password?</button>
            </div>

            {error && (
              <div className="mt-4 flex items-center gap-2 rounded-lg border border-[var(--color-accent-red)]/30 bg-[var(--color-accent-red)]/10 px-3 py-2 text-sm text-[var(--color-accent-red)]">
                <AlertCircle size={15} className="flex-none" /> {error}
              </div>
            )}

            <button
              type="submit" disabled={loading || !username || !password}
              className="mt-5 h-11 w-full rounded-lg bg-[var(--color-accent)] text-sm font-semibold text-white transition-colors hover:bg-[var(--color-accent-hover)] disabled:opacity-40"
            >
              {loading ? 'Signing in…' : 'Sign in'}
            </button>
          </form>

          <div className="mt-4 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)]">
            <button
              onClick={() => setHintsOpen((v) => !v)}
              className="flex w-full items-center justify-between px-4 py-3 text-xs font-medium text-[var(--color-text-secondary)]"
            >
              Demo accounts for this corridor
              <ChevronDown size={14} className={`transition-transform ${hintsOpen ? 'rotate-180' : ''}`} />
            </button>
            {hintsOpen && (
              <div className="border-t border-[var(--color-border)] px-4 py-3 text-xs text-[var(--color-text-secondary)]">
                <p className="mb-2">
                  Password for every account:{' '}
                  <code className="mono rounded bg-white px-1.5 py-0.5">railblock2026</code>
                </p>
                {DEMO_ACCOUNTS.map((a) => (
                  <div key={a.user} className="flex justify-between py-0.5">
                    <span className="mono">{a.user}</span>
                    <span>{a.label}</span>
                  </div>
                ))}
              </div>
            )}
          </div>

          <p className="mt-6 text-center text-xs text-[var(--color-text-muted)]">
            Don't have an account? <span className="font-medium text-[var(--color-accent)]">Contact your admin.</span>
          </p>
        </div>
      </div>

      {/* Right — brand panel */}
      <div className="relative hidden flex-col items-center justify-center overflow-hidden bg-[var(--color-primary)] px-12 lg:flex lg:w-3/5">
        <RailIllustration />
        <div className="mt-10 text-center">
          <div className="text-2xl font-semibold text-white">RailBlock</div>
          <p className="mt-1 text-sm text-white/60">Railway Corridor Operations Platform</p>
        </div>
        <div className="mt-10 flex flex-col gap-3 text-sm text-white/70">
          {['Real-time corridor monitoring', 'Intelligent scheduling optimization', 'Multi-team coordination'].map((f) => (
            <div key={f} className="flex items-center gap-2.5">
              <span className="h-1.5 w-1.5 flex-none rounded-full bg-[var(--color-accent)]" /> {f}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function RailIllustration() {
  const nodes = [[60, 140], [200, 60], [340, 150], [480, 70], [560, 160]]
  return (
    <svg viewBox="0 0 620 220" className="w-full max-w-xl" role="img" aria-label="Abstract rail network illustration">
      {nodes.slice(0, -1).map(([x1, y1], i) => {
        const [x2, y2] = nodes[i + 1]
        return <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke="#3b82f6" strokeOpacity={0.4} strokeWidth={1.5} />
      })}
      <line x1={60} y1={140} x2={560} y2={160} stroke="#3b82f6" strokeOpacity={0.15} strokeWidth={1} />
      {nodes.map(([x, y], i) => (
        <g key={i}>
          <circle cx={x} cy={y} r={5} fill="#3b82f6" opacity={0.9} />
          <circle cx={x} cy={y} r={10} fill="none" stroke="#3b82f6" strokeOpacity={0.3} />
        </g>
      ))}
    </svg>
  )
}

function GoogleGlyph() {
  return (
    <svg width="16" height="16" viewBox="0 0 48 48" aria-hidden="true">
      <path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3c-1.6 4.7-6.1 8-11.3 8-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.9 1.2 8 3.1l5.7-5.7C34.6 6.1 29.6 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.7-.4-3.5z"/>
      <path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.6 16 19 13 24 13c3.1 0 5.9 1.2 8 3.1l5.7-5.7C34.6 7.1 29.6 5 24 5c-7.4 0-13.7 4.1-17 10.1z"/>
      <path fill="#4CAF50" d="M24 44c5.5 0 10.4-2.1 14.1-5.6l-6.5-5.5C29.6 34.6 27 35.5 24 35.5c-5.2 0-9.6-3.3-11.2-8l-6.6 5.1C9.9 39.7 16.4 44 24 44z"/>
      <path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.1-4.1 5.4l6.5 5.5C40.9 36.5 44 30.9 44 24c0-1.3-.1-2.7-.4-3.5z"/>
    </svg>
  )
}

function MicrosoftGlyph() {
  return (
    <svg width="16" height="16" viewBox="0 0 23 23" aria-hidden="true">
      <path fill="#f35325" d="M1 1h10v10H1z" /><path fill="#81bc06" d="M12 1h10v10H12z" />
      <path fill="#05a6f0" d="M1 12h10v10H1z" /><path fill="#ffba08" d="M12 12h10v10H12z" />
    </svg>
  )
}
