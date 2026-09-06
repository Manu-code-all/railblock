import { AlertTriangle, ChevronDown, Send } from 'lucide-react'
import { useEffect, useState } from 'react'
import { api } from '../api'
import { StatusPill } from '../components/Pill'
import type { Dept, RequestRow, Section } from '../types'

interface Props {
  dept: Dept
  roleLabel: string
  sections: Section[]
  days: number
  onChanged: () => void
}

export function DepartmentView({ dept, roleLabel, sections, days, onChanged }: Props) {
  const [rows, setRows] = useState<RequestRow[]>([])
  const [published, setPublished] = useState<any>({ plan: null, blocks: [] })
  const [open, setOpen] = useState(false)
  const [title, setTitle] = useState('')
  const [section, setSection] = useState(sections[0]?.id ?? '')
  const [duration, setDuration] = useState(120)
  const [priority, setPriority] = useState(3)
  const [deadline, setDeadline] = useState(Math.min(3, days - 1))
  const [warning, setWarning] = useState<string | null>(null)
  const [toast, setToast] = useState<string | null>(null)

  const load = () => {
    api.requests().then(setRows)
    api.published().then(setPublished)
  }
  useEffect(load, [dept])
  useEffect(() => setSection(sections[0]?.id ?? ''), [sections])

  const counts = {
    pending: rows.filter((r) => r.status === 'pending').length,
    planned: rows.filter((r) => r.status === 'planned').length,
    deferred: rows.filter((r) => r.status === 'deferred').length,
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault()
    if (!title.trim()) return
    const res = await api.submit({
      section, title: title.trim(), duration, priority,
      deadline_day: deadline,
    })
    setWarning(res.warning)
    setToast(`Submitted as ${res.id}.`)
    setTitle('')
    setOpen(false)
    load()
    onChanged()
    setTimeout(() => setToast(null), 3500)
  }

  const sectionName = (id: string) => sections.find((s) => s.id === id)?.name ?? id
  const myPublished = published.blocks?.filter((b: any) => b.dept === dept) ?? []

  return (
    <div className="mx-auto max-w-4xl px-8 py-10">
      <h1 className="text-[28px] font-extrabold tracking-tight text-[var(--ink)]">{roleLabel}</h1>
      <p className="mt-1 text-[var(--ink-soft)]">Your block requests for this corridor.</p>

      <div className="mt-7 grid grid-cols-4 gap-4">
        {[
          ['Requests', rows.length],
          ['Pending', counts.pending],
          ['Planned', counts.planned],
          ['Deferred', counts.deferred],
        ].map(([label, value]) => (
          <div key={label as string} className="rounded-xl border border-slate-200 bg-white px-4 py-3">
            <div className="text-xs font-medium text-[var(--ink-faint)]">{label}</div>
            <div className="mono mt-0.5 text-2xl font-bold text-[var(--ink)]">{value}</div>
          </div>
        ))}
      </div>

      {toast && (
        <div className="mt-5 rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-2.5 text-sm font-medium text-emerald-800">
          {toast}
        </div>
      )}
      {warning && (
        <div className="mt-3 flex items-start gap-2 rounded-lg border border-amber-200 bg-amber-50 px-4 py-2.5 text-sm text-amber-800">
          <AlertTriangle size={16} className="mt-0.5 flex-none" />
          {warning}
        </div>
      )}

      <div className="mt-6 rounded-xl border border-slate-200 bg-white">
        <button
          onClick={() => setOpen((v) => !v)}
          className="flex w-full items-center justify-between px-5 py-3.5 text-sm font-semibold text-[var(--ink)]"
        >
          Submit a block request
          <ChevronDown size={16} className={`transition-transform ${open ? 'rotate-180' : ''}`} />
        </button>
        {open && (
          <form onSubmit={submit} className="border-t border-slate-100 px-5 py-5">
            <div className="grid grid-cols-3 gap-4">
              <label className="col-span-2 flex flex-col gap-1.5 text-xs font-semibold text-[var(--ink-soft)]">
                Work
                <input
                  value={title} onChange={(e) => setTitle(e.target.value)} maxLength={80}
                  placeholder="e.g. Rail grinding, km 12–18"
                  className="rounded-lg border border-slate-300 px-3 py-2 text-sm font-normal text-[var(--ink)] outline-none focus:border-[var(--navy)]"
                />
              </label>
              <label className="flex flex-col gap-1.5 text-xs font-semibold text-[var(--ink-soft)]">
                Section
                <select
                  value={section} onChange={(e) => setSection(e.target.value)}
                  className="rounded-lg border border-slate-300 px-3 py-2 text-sm font-normal text-[var(--ink)] outline-none focus:border-[var(--navy)]"
                >
                  {sections.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
                </select>
              </label>
            </div>
            <div className="mt-4 grid grid-cols-3 gap-4">
              <label className="flex flex-col gap-1.5 text-xs font-semibold text-[var(--ink-soft)]">
                Duration (minutes)
                <input
                  type="number" min={15} max={480} step={15} value={duration}
                  onChange={(e) => setDuration(Number(e.target.value))}
                  className="mono rounded-lg border border-slate-300 px-3 py-2 text-sm font-normal text-[var(--ink)] outline-none focus:border-[var(--navy)]"
                />
              </label>
              <label className="flex flex-col gap-1.5 text-xs font-semibold text-[var(--ink-soft)]">
                Priority (1 routine · 5 critical)
                <input
                  type="range" min={1} max={5} value={priority}
                  onChange={(e) => setPriority(Number(e.target.value))}
                  className="mt-2.5 accent-[var(--navy)]"
                />
                <span className="mono text-[var(--ink)]">P{priority}</span>
              </label>
              <label className="flex flex-col gap-1.5 text-xs font-semibold text-[var(--ink-soft)]">
                Finish by day
                <input
                  type="number" min={0} max={days - 1} value={deadline}
                  onChange={(e) => setDeadline(Number(e.target.value))}
                  className="mono rounded-lg border border-slate-300 px-3 py-2 text-sm font-normal text-[var(--ink)] outline-none focus:border-[var(--navy)]"
                />
              </label>
            </div>
            <button
              type="submit"
              className="mt-5 flex items-center gap-2 rounded-lg bg-[var(--navy)] px-4 py-2.5 text-sm font-semibold text-white transition-opacity hover:opacity-90"
            >
              <Send size={14} /> Submit request
            </button>
          </form>
        )}
      </div>

      <h2 className="mb-3 mt-8 text-sm font-bold uppercase tracking-wide text-[var(--ink-soft)]">My requests</h2>
      {rows.length === 0 ? (
        <p className="rounded-lg bg-slate-100 px-4 py-3 text-sm text-[var(--ink-soft)]">
          No requests yet. Submit one above.
        </p>
      ) : (
        <div className="overflow-hidden rounded-xl border border-slate-200 bg-white">
          {rows.map((r, i) => (
            <div
              key={r.id}
              className={`grid grid-cols-[64px_1fr_auto_auto] items-center gap-4 px-5 py-3.5 ${i > 0 ? 'border-t border-slate-100' : ''}`}
            >
              <span className="mono text-sm font-bold text-[var(--ink)]">{r.id}</span>
              <div>
                <div className="text-sm font-medium text-[var(--ink)]">{r.title}</div>
                <div className="text-xs text-[var(--ink-faint)]">
                  {sectionName(r.section)} · {r.duration} min · P{r.priority} · by day {r.deadline_day}
                </div>
              </div>
              <StatusPill status={r.status} />
              {r.status === 'pending' ? (
                <button
                  onClick={() => api.withdraw(r.id).then(() => { load(); onChanged() })}
                  className="rounded-lg border border-slate-300 px-3 py-1.5 text-xs font-semibold text-[var(--ink-soft)] hover:bg-slate-50"
                >
                  Withdraw
                </button>
              ) : <span />}
            </div>
          ))}
        </div>
      )}

      {published.plan && (
        <>
          <h2 className="mb-3 mt-8 text-sm font-bold uppercase tracking-wide text-[var(--ink-soft)]">Published block order</h2>
          {myPublished.length === 0 ? (
            <p className="text-sm text-[var(--ink-faint)]">The live block order contains no work for your department.</p>
          ) : (
            <div className="overflow-hidden rounded-xl border border-slate-200 bg-white">
              {myPublished.map((b: any, i: number) => (
                <div key={b.request_id} className={`grid grid-cols-[50px_70px_1fr_1fr] gap-4 px-5 py-3 text-sm ${i > 0 ? 'border-t border-slate-100' : ''}`}>
                  <span className="mono font-semibold">{b.request_id}</span>
                  <span className="mono text-[var(--ink-faint)]">Day {b.day}</span>
                  <span className="text-[var(--ink-soft)]">{b.sectionName}</span>
                  <span>{b.title}</span>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  )
}
