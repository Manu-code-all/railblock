import { Train } from 'lucide-react'
import type { Dept } from '../types'

export const ROLES: { label: string; dept: Dept | null }[] = [
  { label: 'Engineering (P.Way)', dept: 'ENGG' },
  { label: 'Signalling & Telecom', dept: 'S&T' },
  { label: 'Traction (OHE)', dept: 'TRD' },
  { label: 'Section controller', dept: null },
]

interface Props {
  role: string
  setRole: (r: string) => void
  sectionCount: number
  days: number
  pendingCount: number
  publishedPlanId: number | null
}

export function Sidebar({ role, setRole, sectionCount, days, pendingCount, publishedPlanId }: Props) {
  return (
    <aside className="flex h-full w-64 flex-none flex-col gap-6 border-r border-slate-200 bg-white px-5 py-6">
      <div className="flex items-center gap-2.5">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-[var(--navy)] text-white">
          <Train size={17} />
        </div>
        <div>
          <div className="text-[15px] font-extrabold leading-tight text-[var(--ink)]">RailBlock</div>
          <div className="text-[11px] leading-tight text-[var(--ink-faint)]">Block planning</div>
        </div>
      </div>

      <nav className="flex flex-col gap-1">
        <div className="mb-1 px-1 text-[11px] font-semibold uppercase tracking-wide text-[var(--ink-faint)]">
          Signed in as
        </div>
        {ROLES.map((r) => (
          <button
            key={r.label}
            onClick={() => setRole(r.label)}
            className={`rounded-lg px-3 py-2 text-left text-sm font-medium transition-colors ${
              role === r.label
                ? 'bg-[var(--navy)] text-white shadow-sm'
                : 'text-[var(--ink-soft)] hover:bg-slate-100'
            }`}
          >
            {r.label}
          </button>
        ))}
      </nav>

      <div className="mt-auto flex flex-col gap-2 border-t border-slate-200 pt-4 text-xs text-[var(--ink-soft)]">
        <div className="flex justify-between">
          <span>Corridor</span>
          <span className="mono font-semibold text-[var(--ink)]">{sectionCount} sections</span>
        </div>
        <div className="flex justify-between">
          <span>Horizon</span>
          <span className="mono font-semibold text-[var(--ink)]">{days} days</span>
        </div>
        <div className="flex justify-between">
          <span>Pending</span>
          <span className="mono font-semibold text-[var(--ink)]">{pendingCount}</span>
        </div>
        <div className="flex justify-between">
          <span>Block order</span>
          <span className="mono font-semibold text-[var(--ink)]">
            {publishedPlanId ? `plan #${publishedPlanId}` : 'none'}
          </span>
        </div>
      </div>
    </aside>
  )
}
