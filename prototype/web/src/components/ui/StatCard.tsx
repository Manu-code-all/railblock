import type { LucideIcon } from 'lucide-react'
import { ArrowDown, ArrowUp } from 'lucide-react'

interface Props {
  icon: LucideIcon
  color: string
  label: string
  value: string | number
  trend?: { direction: 'up' | 'down'; label: string; tone?: 'green' | 'amber' | 'red' }
  sparkline?: number[]
  subtitle?: string
}

export function StatCard({ icon: Icon, color, label, value, trend, sparkline, subtitle }: Props) {
  const trendColor = trend?.tone === 'red' ? 'var(--color-accent-red)'
    : trend?.tone === 'amber' ? 'var(--color-accent-amber)'
    : 'var(--color-accent-green)'

  return (
    <div className="group rounded-xl border border-[var(--color-border)] bg-[var(--color-surface-elevated)] p-4 shadow-[var(--shadow-sm)] transition-all duration-150 hover:-translate-y-0.5 hover:shadow-[var(--shadow-md)]">
      <div className="flex items-start justify-between">
        <div
          className="flex h-9 w-9 items-center justify-center rounded-full"
          style={{ background: `color-mix(in srgb, ${color} 14%, transparent)` }}
        >
          <Icon size={17} style={{ color }} aria-hidden="true" />
        </div>
        {sparkline && sparkline.length > 1 && <Sparkline data={sparkline} color={color} />}
      </div>

      <div className="mt-3 text-[12px] font-medium text-[var(--color-text-secondary)]">{label}</div>
      <div className="mono mt-0.5 text-[28px] font-bold leading-none text-[var(--color-text-primary)]">{value}</div>

      {subtitle && <div className="mt-1 text-[12px] text-[var(--color-text-muted)]">{subtitle}</div>}

      {trend && (
        <div className="mt-2 flex items-center gap-1 text-[12px] font-medium" style={{ color: trendColor }}>
          {trend.direction === 'up' ? <ArrowUp size={12} /> : <ArrowDown size={12} />}
          {trend.label}
        </div>
      )}
    </div>
  )
}

function Sparkline({ data, color }: { data: number[]; color: string }) {
  const w = 60, h = 24
  const max = Math.max(...data, 1)
  const min = Math.min(...data, 0)
  const range = max - min || 1
  const points = data
    .map((v, i) => `${(i / (data.length - 1)) * w},${h - ((v - min) / range) * h}`)
    .join(' ')
  return (
    <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`} aria-hidden="true">
      <polyline points={points} fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round" opacity={0.7} />
    </svg>
  )
}
