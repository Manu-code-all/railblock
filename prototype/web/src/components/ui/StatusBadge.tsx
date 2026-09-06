export type StatusVariant = 'requested' | 'pending' | 'approved' | 'denied' | 'scheduled' | 'optimal'

const VARIANT: Record<StatusVariant, { bg: string; fg: string; glow?: boolean }> = {
  requested: { bg: 'rgba(59,130,246,0.12)', fg: 'var(--color-accent)' },
  pending: { bg: 'rgba(245,158,11,0.12)', fg: 'var(--color-accent-amber)' },
  approved: { bg: 'rgba(16,185,129,0.12)', fg: 'var(--color-accent-green)' },
  denied: { bg: 'rgba(239,68,68,0.12)', fg: 'var(--color-accent-red)' },
  scheduled: { bg: 'rgba(139,92,246,0.12)', fg: 'var(--color-accent-purple)' },
  optimal: { bg: 'rgba(16,185,129,0.14)', fg: 'var(--color-accent-green)', glow: true },
}

export function StatusBadge({ variant, children }: { variant: StatusVariant; children: React.ReactNode }) {
  const v = VARIANT[variant]
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[11px] font-semibold transition-transform hover:scale-105 ${v.glow ? 'ring-1 ring-[color:var(--color-accent-green)]/30' : ''}`}
      style={{ background: v.bg, color: v.fg }}
    >
      <span className="h-1.5 w-1.5 rounded-full" style={{ background: v.fg }} />
      {children}
    </span>
  )
}
