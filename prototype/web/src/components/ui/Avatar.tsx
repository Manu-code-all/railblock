function initials(name: string) {
  const parts = name.replace(/[._]/g, ' ').trim().split(/\s+/)
  return (parts[0]?.[0] ?? '').toUpperCase() + (parts[1]?.[0] ?? '').toUpperCase()
}

export function Avatar({ name, size = 28, status }: { name: string; size?: number; status?: 'online' | 'offline' }) {
  return (
    <span className="relative inline-flex flex-none" style={{ width: size, height: size }}>
      <span
        className="flex items-center justify-center rounded-full bg-[var(--color-primary)] font-semibold text-white"
        style={{ width: size, height: size, fontSize: size * 0.38 }}
      >
        {initials(name) || '?'}
      </span>
      {status && (
        <span
          className="absolute -bottom-0.5 -right-0.5 rounded-full border-2 border-[var(--color-surface-elevated)]"
          style={{
            width: size * 0.34, height: size * 0.34,
            background: status === 'online' ? 'var(--color-accent-green)' : 'var(--color-text-muted)',
          }}
          aria-label={status}
        />
      )}
    </span>
  )
}
