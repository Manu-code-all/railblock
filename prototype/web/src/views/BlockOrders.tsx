import { Download } from 'lucide-react'
import { useEffect, useState } from 'react'
import { api } from '../api'
import { DeptTag } from '../components/Pill'

export function BlockOrders() {
  const [data, setData] = useState<{ plan: any; blocks: any[] } | null>(null)

  useEffect(() => { api.published().then(setData) }, [])

  if (!data) return null

  return (
    <div>

      {!data.plan ? (
        <p className="mt-6 rounded-[8px] bg-[var(--surface-2)] px-4 py-3 text-sm text-[var(--ink-soft)]">
          No block order published yet.
        </p>
      ) : (
        <>
          <p className="mt-1 text-[var(--ink-soft)]">
            Plan #{data.plan.id} · published {data.plan.created_at} · {data.blocks.length} blocks
          </p>

          <div className="mt-6 overflow-hidden rounded-[12px] border border-[var(--hairline)] bg-[var(--surface-1)]">
            <table className="w-full text-sm">
              <thead className="bg-[var(--surface-2)] text-xs uppercase tracking-wide text-[var(--ink-faint)]">
                <tr>
                  <th className="px-4 py-2.5 text-left">Day</th>
                  <th className="px-4 py-2.5 text-left">Time</th>
                  <th className="px-4 py-2.5 text-left">Section</th>
                  <th className="px-4 py-2.5 text-left">Department</th>
                  <th className="px-4 py-2.5 text-left">Work</th>
                  <th className="px-4 py-2.5 text-left">Request</th>
                </tr>
              </thead>
              <tbody>
                {data.blocks.map((b) => {
                  const s = b.start % 1440, e = b.end % 1440
                  const clock = `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}–${String(Math.floor(e / 60)).padStart(2, '0')}:${String(e % 60).padStart(2, '0')}`
                  return (
                    <tr key={b.request_id} className="border-t border-[var(--hairline)]">
                      <td className="mono px-4 py-2.5">{b.day}</td>
                      <td className="mono px-4 py-2.5">{clock}</td>
                      <td className="px-4 py-2.5">{b.sectionName}</td>
                      <td className="px-4 py-2.5"><DeptTag dept={b.dept} name={b.deptName} /></td>
                      <td className="px-4 py-2.5">{b.title}</td>
                      <td className="mono px-4 py-2.5 font-semibold">{b.request_id}</td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>

          <button
            onClick={() => api.exportCsv()}
            className="mt-5 inline-flex items-center gap-2 rounded-[8px] bg-[var(--lavender)] px-4 py-2.5 text-sm font-semibold text-white hover:opacity-90"
          >
            <Download size={14} /> Download as CSV
          </button>
        </>
      )}
    </div>
  )
}
