import type { LucideIcon } from 'lucide-react'

interface Props {
  icon: LucideIcon
  heading: string
  description: string
  actionLabel?: string
  onAction?: () => void
  secondaryLabel?: string
  onSecondary?: () => void
}

export function EmptyState({ icon: Icon, heading, description, actionLabel, onAction, secondaryLabel, onSecondary }: Props) {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-[var(--color-border-strong)] bg-[var(--color-surface-elevated)] px-8 py-14 text-center">
      <div className="flex h-14 w-14 items-center justify-center rounded-full bg-[var(--color-surface)]">
        <Icon size={26} className="text-[var(--color-text-muted)]" aria-hidden="true" />
      </div>
      <h3 className="mt-4 text-base font-semibold text-[var(--color-text-primary)]">{heading}</h3>
      <p className="mt-1 max-w-sm text-sm text-[var(--color-text-secondary)]">{description}</p>
      {actionLabel && (
        <button
          onClick={onAction}
          className="mt-5 rounded-lg bg-[var(--color-accent)] px-4 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-[var(--color-accent-hover)]"
        >
          {actionLabel}
        </button>
      )}
      {secondaryLabel && (
        <button onClick={onSecondary} className="mt-2 text-sm font-medium text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)]">
          {secondaryLabel}
        </button>
      )}
    </div>
  )
}
