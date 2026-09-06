import { LogOut, Train } from 'lucide-react'
import type { Session } from '../types'

interface Props {
  user: Session
  onLogout: () => void
  sectionCount: number
  days: number
  pendingCount: number
  publishedPlanId: number | null
}

export function Sidebar({ user, onLogout, sectionCount, days, pendingCount, publishedPlanId }: Props) {
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

      <div className="rounded-xl border border-slate-200 bg-[var(--surface-2)] px-3.5 py-3">
        <div className="text-[10px] font-semibold uppercase tracking-wide text-[var(--ink-faint)]">Signed in as</div>
        <div className="mt-1 text-sm font-bold text-[var(--ink)]">{user.display_name}</div>
        <div className="mono text-xs text-[var(--ink-faint)]">{user.username}</div>
        <button
          onClick={onLogout}
          className="mt-2.5 flex items-center gap-1.5 text-xs font-semibold text-[var(--ink-soft)] hover:text-[var(--red)]"
        >
          <LogOut size={13} /> Log out
        </button>
      </div>

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
