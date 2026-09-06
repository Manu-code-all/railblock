import type { Meta, Session } from '../types'

function Row({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div className="flex items-center justify-between border-b border-[var(--color-border)] py-3 last:border-0">
      <span className="text-sm text-[var(--color-text-secondary)]">{label}</span>
      <span className="mono text-sm font-medium text-[var(--color-text-primary)]">{value}</span>
    </div>
  )
}

export function Settings({ user, meta }: { user: Session; meta: Meta }) {
  return (
    <div className="mx-auto grid max-w-2xl gap-5">
      <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface-elevated)] p-5 shadow-[var(--shadow-sm)]">
        <h2 className="mb-1 text-sm font-semibold text-[var(--color-text-primary)]">Account</h2>
        <Row label="Signed in as" value={user.display_name} />
        <Row label="Username" value={user.username} />
        <Row label="Role" value={user.dept ?? 'Section controller'} />
      </div>

      <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-surface-elevated)] p-5 shadow-[var(--shadow-sm)]">
        <h2 className="mb-1 text-sm font-semibold text-[var(--color-text-primary)]">Corridor</h2>
        <Row label="Sections" value={meta.sectionCount} />
        <Row label="Traffic-free windows" value={meta.windowCount} />
        <Row label="Planning horizon" value={`${meta.days} days`} />
        <Row label="Published block order" value={meta.published ? `plan #${meta.published.id}` : 'none'} />
      </div>

      <p className="rounded-xl border border-dashed border-[var(--color-border-strong)] bg-[var(--color-surface)] p-4 text-xs text-[var(--color-text-muted)]">
        This is a demo-scale settings page — it shows what's real about your account and corridor rather than
        offering controls (notification preferences, integrations, billing) that don't exist yet in RailBlock.
      </p>
    </div>
  )
}
