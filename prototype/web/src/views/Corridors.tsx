import { useEffect, useState } from 'react'
import { api } from '../api'
import type { Meta, WindowRow } from '../types'

export function Corridors({ meta }: { meta: Meta }) {
  const [windows, setWindows] = useState<WindowRow[] | null>(null)

  useEffect(() => { api.windows().then(setWindows) }, [])

  return (
    <div>
      <p className="mb-4 text-sm text-[var(--color-text-secondary)]">
        RailBlock plans one corridor at a time. This is the corridor currently loaded — swap it with{' '}
        <code className="mono rounded bg-[var(--color-surface)] px-1.5 py-0.5">python -m railblock.load</code>.
      </p>
      <div className="overflow-hidden rounded-xl border border-[var(--color-border)] bg-[var(--color-surface-elevated)] shadow-[var(--shadow-sm)]">
        <table className="w-full text-sm">
          <thead className="bg-[var(--color-surface)] text-[11px] uppercase tracking-wide text-[var(--color-text-muted)]">
            <tr>
              <th className="px-4 py-2.5 text-left">Section</th>
              <th className="px-4 py-2.5 text-left">ID</th>
              <th className="px-4 py-2.5 text-left">Traffic-free windows</th>
            </tr>
          </thead>
          <tbody>
            {meta.sections.map((s, i) => (
              <tr key={s.id} className={`transition-colors hover:bg-[var(--color-surface)] ${i % 2 ? 'bg-[var(--color-surface)]/40' : ''}`}>
                <td className="px-4 py-3 font-medium text-[var(--color-text-primary)]">{s.name}</td>
                <td className="mono px-4 py-3 text-[var(--color-text-muted)]">{s.id}</td>
                <td className="mono px-4 py-3 text-[var(--color-text-secondary)]">
                  {windows ? windows.filter((w) => w.section === s.id).length : '…'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
