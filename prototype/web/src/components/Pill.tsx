const STATUS_STYLE: Record<string, string> = {
  pending: 'bg-[var(--surface-2)] text-[var(--ink-soft)]',
  planned: 'bg-[var(--green)]/10 text-[var(--green)]',
  deferred: 'bg-[var(--amber)]/10 text-[var(--amber)]',
}

export function StatusPill({ status }: { status: string }) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
        STATUS_STYLE[status] ?? 'bg-[var(--surface-2)] text-[var(--ink-soft)]'
      }`}
    >
      {status}
    </span>
  )
}

const DEPT_COLOR: Record<string, string> = {
  ENGG: 'var(--blue)',
  'S&T': 'var(--green)',
  TRD: 'var(--amber)',
}

export function DeptTag({ dept, name }: { dept: string; name: string }) {
  const color = DEPT_COLOR[dept] ?? 'var(--ink-soft)'
  return (
    <span className="inline-flex items-center gap-1.5 text-xs font-medium" style={{ color }}>
      <span className="h-2 w-2 rounded-full" style={{ background: color }} />
      {name}
    </span>
  )
}
