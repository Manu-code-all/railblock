import { Bell, Search } from 'lucide-react'
import { useState } from 'react'
import type { Session } from '../../types'
import { Avatar } from './Avatar'

interface Props {
  title: string
  breadcrumb?: string
  searchPlaceholder?: string
  onSearch?: (q: string) => void
  notificationCount?: number
  notificationLabel?: string
  user: Session
  right?: React.ReactNode
}

export function Toolbar({ title, breadcrumb, searchPlaceholder, onSearch, notificationCount, notificationLabel, user, right }: Props) {
  const [notifOpen, setNotifOpen] = useState(false)

  return (
    <div className="flex h-16 flex-none items-center gap-4 border-b border-[var(--color-border)] bg-[var(--color-surface-elevated)] px-6">
      <div className="min-w-0">
        {breadcrumb && <div className="truncate text-[11px] text-[var(--color-text-muted)]">{breadcrumb}</div>}
        <h1 className="truncate text-[20px] font-semibold leading-tight text-[var(--color-text-primary)]">{title}</h1>
      </div>

      {onSearch && (
        <div className="mx-auto hidden max-w-sm flex-1 md:block">
          <div className="flex items-center gap-2 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-2">
            <Search size={15} className="text-[var(--color-text-muted)]" />
            <input
              onChange={(e) => onSearch(e.target.value)}
              placeholder={searchPlaceholder ?? 'Search…'}
              className="w-full bg-transparent text-sm outline-none placeholder:text-[var(--color-text-muted)]"
            />
          </div>
        </div>
      )}

      <div className="ml-auto flex flex-none items-center gap-3">
        {right}

        <div className="relative">
          <button
            onClick={() => setNotifOpen((v) => !v)}
            aria-label="Notifications"
            className="relative flex h-9 w-9 items-center justify-center rounded-lg text-[var(--color-text-secondary)] hover:bg-[var(--color-surface)]"
          >
            <Bell size={17} />
            {!!notificationCount && (
              <span className="absolute -right-0.5 -top-0.5 flex h-4 min-w-4 items-center justify-center rounded-full bg-[var(--color-accent-red)] px-1 text-[10px] font-bold text-white">
                {notificationCount}
              </span>
            )}
          </button>
          {notifOpen && (
            <div className="absolute right-0 top-11 z-20 w-64 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface-elevated)] p-3 text-sm shadow-[var(--shadow-lg)]">
              {notificationCount
                ? <p className="text-[var(--color-text-primary)]">{notificationLabel}</p>
                : <p className="text-[var(--color-text-muted)]">Nothing needs your attention.</p>}
            </div>
          )}
        </div>

        <div className="flex items-center gap-2">
          <Avatar name={user.display_name} size={30} />
          <span className="hidden text-sm font-medium text-[var(--color-text-primary)] lg:inline">{user.display_name}</span>
        </div>
      </div>
    </div>
  )
}
