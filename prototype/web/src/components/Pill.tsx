const STATUS_STYLE: Record<string, string> = {
  pending: 'bg-slate-100 text-slate-600',
  planned: 'bg-emerald-50 text-emerald-700',
  deferred: 'bg-amber-50 text-amber-700',
}

export function StatusPill({ status }: { status: string }) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold ${
        STATUS_STYLE[status] ?? 'bg-slate-100 text-slate-600'
      }`}
    >
      {status}
    </span>
  )
}

export function DeptTag({ dept, name }: { dept: string; name: string }) {
  const color =
    dept === 'ENGG' ? '#2E6DA4' : dept === 'S&T' ? '#1E8449' : '#B8790A'
  return (
    <span className="inline-flex items-center gap-1.5 text-xs font-semibold" style={{ color }}>
      <span className="h-2 w-2 rounded-full" style={{ background: color }} />
      {name}
    </span>
  )
}
