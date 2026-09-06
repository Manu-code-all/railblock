import type { LucideIcon } from 'lucide-react'
import { ChevronsLeft, ChevronsRight, LogOut, Train } from 'lucide-react'
import { useState } from 'react'
import type { Session } from '../../types'
import { Avatar } from './Avatar'

export interface NavItem {
  key: string
  label: string
  icon: LucideIcon
  group: 'Operations' | 'Admin'
}

interface Props {
  items: NavItem[]
  active: string
  onSelect: (key: string) => void
  user: Session
  onLogout: () => void
}

export function Sidebar({ items, active, onSelect, user, onLogout }: Props) {
  const [expanded, setExpanded] = useState(true)
  const groups: NavItem['group'][] = ['Operations', 'Admin']

  return (
    <aside
      className="flex h-full flex-none flex-col border-r border-[var(--color-border)] bg-[var(--color-primary)] py-4 text-white transition-[width] duration-200 ease-out"
      style={{ width: expanded ? 240 : 60 }}
    >
      <div className={`flex items-center gap-2.5 px-4 ${expanded ? '' : 'justify-center px-0'}`}>
        <div className="flex h-8 w-8 flex-none items-center justify-center rounded-lg bg-[var(--color-accent)]">
          <Train size={17} />
        </div>
        {expanded && (
          <div className="min-w-0">
            <div className="truncate text-[15px] font-semibold leading-tight">RailBlock</div>
            <div className="truncate text-[11px] leading-tight text-white/50">Block planning</div>
          </div>
        )}
      </div>

      <button
        onClick={() => setExpanded((v) => !v)}
        aria-label={expanded ? 'Collapse sidebar' : 'Expand sidebar'}
        className="mx-4 mt-3 flex h-8 items-center justify-center gap-2 rounded-lg text-white/50 hover:bg-white/10 hover:text-white"
      >
        {expanded ? <ChevronsLeft size={15} /> : <ChevronsRight size={15} />}
      </button>

      <nav className="mt-4 flex flex-1 flex-col gap-4 overflow-y-auto px-2">
        {groups.map((g) => {
          const groupItems = items.filter((i) => i.group === g)
          if (groupItems.length === 0) return null
          return (
            <div key={g}>
              {expanded && (
                <div className="mb-1 px-2 text-[10px] font-semibold uppercase tracking-wide text-white/35">{g}</div>
              )}
              <div className="flex flex-col gap-0.5">
                {groupItems.map((item) => {
                  const isActive = active === item.key
                  return (
                    <button
                      key={item.key}
                      onClick={() => onSelect(item.key)}
                      title={expanded ? undefined : item.label}
                      className={`group relative flex items-center gap-3 rounded-lg py-2 text-sm font-medium transition-colors ${
                        expanded ? 'px-3' : 'justify-center px-0'
                      } ${isActive ? 'bg-white/10 text-white' : 'text-white/60 hover:bg-white/5 hover:text-white'}`}
                    >
                      {isActive && <span className="absolute left-0 top-1 bottom-1 w-[3px] rounded-r bg-[var(--color-accent)]" />}
                      <item.icon size={17} className="flex-none" aria-hidden="true" />
                      {expanded && <span className="truncate">{item.label}</span>}
                      {!expanded && (
                        <span className="pointer-events-none absolute left-full ml-2 whitespace-nowrap rounded-md bg-[var(--color-primary-light)] px-2 py-1 text-xs opacity-0 shadow-[var(--shadow-md)] transition-opacity group-hover:opacity-100">
                          {item.label}
                        </span>
                      )}
                    </button>
                  )
                })}
              </div>
            </div>
          )
        })}
      </nav>

      <div className={`mt-auto flex items-center gap-2.5 border-t border-white/10 px-3 pt-3 ${expanded ? '' : 'justify-center px-0'}`}>
        <Avatar name={user.display_name} status="online" />
        {expanded && (
          <div className="min-w-0 flex-1">
            <div className="truncate text-xs font-semibold">{user.display_name}</div>
            <button onClick={onLogout} className="flex items-center gap-1 text-[11px] text-white/50 hover:text-white">
              <LogOut size={11} /> Log out
            </button>
          </div>
        )}
      </div>
    </aside>
  )
}
