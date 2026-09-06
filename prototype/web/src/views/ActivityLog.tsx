import { useEffect, useMemo, useState } from 'react'
import { api } from '../api'
import type { ActivityRow } from '../types'

export function ActivityLog() {
  const [rows, setRows] = useState<ActivityRow[]>([])
  const [actor, setActor] = useState('All')

  useEffect(() => { api.activity(200).then(setRows) }, [])

  const actors = useMemo(() => ['All', ...Array.from(new Set(rows.map((r) => r.actor))).sort()], [rows])
  const filtered = actor === 'All' ? rows : rows.filter((r) => r.actor === actor)

  return (
    <div className="mx-auto max-w-5xl px-8 py-10">
      <h1 className="text-[28px] font-semibold leading-[1.2] tracking-[-0.6px] text-[var(--ink)]">Activity log</h1>

      {rows.length === 0 ? (
        <p className="mt-6 rounded-[8px] bg-[var(--surface-2)] px-4 py-3 text-sm text-[var(--ink-soft)]">No activity yet.</p>
      ) : (
        <>
          <select
            value={actor} onChange={(e) => setActor(e.target.value)}
            className="mt-6 rounded-[8px] border border-[var(--hairline-strong)] px-3 py-2 text-sm outline-none focus:border-[var(--lavender)]"
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
                    <td className="px-4 py-2.5">{r.action}</td>
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
