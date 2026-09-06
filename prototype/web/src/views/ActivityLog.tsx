import { useEffect, useMemo, useState } from 'react'
import { api } from '../api'
import type { ActivityRow } from '../types'

const ACTION_COLOR: Record<string, string> = {
  'submitted request': 'var(--blue)',
  'withdrew request': 'var(--ink-faint)',
  'marked deferred': 'var(--amber)',
  'solved a plan': 'var(--lavender)',
  'published block order': 'var(--green)',
  'seeded corridor': 'var(--ink-faint)',
  'imported corridor': 'var(--ink-faint)',
}

function actionColor(action: string) {
  return ACTION_COLOR[action] ?? 'var(--ink-soft)'
}

function ActionBadge({ action }: { action: string }) {
  const color = actionColor(action)
  return (
    <span
      className="inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium"
      style={{ background: `color-mix(in srgb, ${color} 12%, transparent)`, color }}
    >
      <span className="h-1.5 w-1.5 rounded-full" style={{ background: color }} />
      {action}
    </span>
  )
}

/** Hour key like "26 Feb 14:00", bucketing every row's timestamp to its hour. */
function hourKey(at: string) {
  const d = new Date(at.replace(' ', 'T'))
  d.setMinutes(0, 0, 0)
  return d
}

function BarChart({ rows }: { rows: ActivityRow[] }) {
  if (rows.length === 0) return null

  const times = rows.map((r) => hourKey(r.at).getTime())
  const min = Math.min(...times)
  const max = Math.max(...times)
  const hourMs = 3600_000
  const bucketCount = Math.max(1, Math.round((max - min) / hourMs) + 1)
  const buckets = Array.from({ length: bucketCount }, (_, i) => ({
    t: min + i * hourMs,
    count: 0,
  }))
  for (const t of times) {
    const idx = Math.round((t - min) / hourMs)
    buckets[idx].count++
  }

  const W = 640, H = 180, PAD_L = 28, PAD_B = 20
  const plotW = W - PAD_L - 8, plotH = H - PAD_B - 10
  const maxCount = Math.max(...buckets.map((b) => b.count), 1)
  const barW = Math.min(28, (plotW / buckets.length) * 0.6)
  const step = plotW / buckets.length

  const yTicks = 4
  const fmtHour = (t: number) =>
    new Date(t).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })

  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label="Activity volume by hour">
      {Array.from({ length: yTicks + 1 }).map((_, i) => {
        const v = Math.round((maxCount / yTicks) * i)
        const y = 10 + plotH - (plotH / yTicks) * i
        return (
          <g key={i}>
            <line x1={PAD_L} x2={W - 4} y1={y} y2={y} stroke="var(--hairline)" strokeWidth={1} />
            <text x={0} y={y + 3} fontSize={9} fill="var(--ink-faint)" fontFamily="IBM Plex Mono">{v}</text>
          </g>
        )
      })}
      {buckets.map((b, i) => {
        const h = (b.count / maxCount) * plotH
        const x = PAD_L + i * step + (step - barW) / 2
        const y = 10 + plotH - h
        return (
          <g key={i}>
            <rect x={x} y={y} width={barW} height={Math.max(h, b.count ? 2 : 0)} rx={3} fill="var(--lavender)" />
            {(i === 0 || i === buckets.length - 1 || i === Math.floor(buckets.length / 2)) && (
              <text
                x={x + barW / 2} y={H - 4} fontSize={9} textAnchor="middle"
                fill="var(--ink-faint)" fontFamily="IBM Plex Mono"
              >
                {fmtHour(b.t)}
              </text>
            )}
          </g>
        )
      })}
    </svg>
  )
}

export function ActivityLog() {
  const [rows, setRows] = useState<ActivityRow[]>([])
  const [actor, setActor] = useState('All')

  useEffect(() => { api.activity(200).then(setRows) }, [])

  const actors = useMemo(() => ['All', ...Array.from(new Set(rows.map((r) => r.actor))).sort()], [rows])
  const filtered = actor === 'All' ? rows : rows.filter((r) => r.actor === actor)

  const breakdown = useMemo(() => {
    const counts = new Map<string, number>()
    for (const r of rows) counts.set(r.action, (counts.get(r.action) ?? 0) + 1)
    return Array.from(counts.entries())
      .map(([action, count]) => ({ action, count, pct: (count / rows.length) * 100 }))
      .sort((a, b) => b.count - a.count)
  }, [rows])

  return (
    <div>

      {rows.length === 0 ? (
        <p className="mt-6 rounded-[8px] bg-[var(--surface-2)] px-4 py-3 text-sm text-[var(--ink-soft)]">No activity yet.</p>
      ) : (
        <>
          <div className="mt-6 grid grid-cols-[280px_1fr] overflow-hidden rounded-[12px] border border-[var(--hairline)] bg-[var(--surface-1)]">
            <div className="border-r border-[var(--hairline)] p-6">
              <div className="mono text-4xl font-semibold text-[var(--ink)]">{rows.length}</div>
              <div className="mt-1 text-xs font-medium uppercase tracking-wide text-[var(--ink-faint)]">Actions logged</div>
              <div className="mt-5 flex flex-col gap-2.5">
                {breakdown.map((b) => (
                  <div key={b.action} className="flex items-center gap-2 text-sm">
                    <span className="h-2 w-2 flex-none rounded-full" style={{ background: actionColor(b.action) }} />
                    <span className="flex-1 truncate text-[var(--ink-muted)]">{b.action}</span>
                    <span className="mono font-medium text-[var(--ink)]">{b.count}</span>
                    <span className="mono w-11 text-right text-[var(--ink-faint)]">{b.pct.toFixed(0)}%</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="flex items-center p-6">
              <BarChart rows={rows} />
            </div>
          </div>

          <select
            value={actor} onChange={(e) => setActor(e.target.value)}
            className="mt-6 rounded-[8px] border border-[var(--hairline-strong)] bg-[var(--surface-1)] px-3 py-2 text-sm outline-none focus:border-[var(--lavender)]"
          >
            {actors.map((a) => <option key={a} value={a}>{a}</option>)}
          </select>

          <div className="mt-4 overflow-hidden rounded-[12px] border border-[var(--hairline)] bg-[var(--surface-1)]">
            <table className="w-full text-sm">
              <thead className="bg-[var(--surface-2)] text-xs uppercase tracking-wide text-[var(--ink-faint)]">
                <tr>
                  <th className="px-4 py-2.5 text-left">When</th>
                  <th className="px-4 py-2.5 text-left">Actor</th>
                  <th className="px-4 py-2.5 text-left">Action</th>
                  <th className="px-4 py-2.5 text-left">Detail</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((r) => (
                  <tr key={r.id} className="border-t border-[var(--hairline)]">
                    <td className="mono px-4 py-2.5 text-[var(--ink-faint)]">{r.at}</td>
                    <td className="mono px-4 py-2.5 font-semibold">{r.actor}</td>
                    <td className="px-4 py-2.5"><ActionBadge action={r.action} /></td>
                    <td className="px-4 py-2.5 text-[var(--ink-soft)]">{r.detail}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  )
}
