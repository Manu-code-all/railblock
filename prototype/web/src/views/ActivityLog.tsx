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
      <h1 className="text-[28px] font-extrabold tracking-tight text-[var(--ink)]">Activity log</h1>

      {rows.length === 0 ? (
        <p className="mt-6 rounded-lg bg-slate-100 px-4 py-3 text-sm text-[var(--ink-soft)]">No activity yet.</p>
      ) : (
        <>
          <select
            value={actor} onChange={(e) => setActor(e.target.value)}
            className="mt-6 rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:border-[var(--navy)]"
          >
            {actors.map((a) => <option key={a} value={a}>{a}</option>)}
          </select>

          <div className="mt-4 overflow-hidden rounded-xl border border-slate-200 bg-white">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 text-xs uppercase tracking-wide text-[var(--ink-faint)]">
                <tr>
                  <th className="px-4 py-2.5 text-left">When</th>
                  <th className="px-4 py-2.5 text-left">Actor</th>
                  <th className="px-4 py-2.5 text-left">Action</th>
                  <th className="px-4 py-2.5 text-left">Detail</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((r) => (
                  <tr key={r.id} className="border-t border-slate-100">
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
