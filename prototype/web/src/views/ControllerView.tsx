import { AlertOctagon, CheckCircle2, ChevronDown, Loader2, Rocket, Sparkles } from 'lucide-react'
import { useEffect, useState } from 'react'
import { api } from '../api'
import { Gantt } from '../components/Gantt'
import type { Explanation, Section, SolveResult, WindowRow } from '../types'

interface Props {
  sections: Section[]
  onChanged: () => void
}

export function ControllerView({ sections, onChanged }: Props) {
  const [urgency, setUrgency] = useState(0.5)
  const [strict, setStrict] = useState(false)
  const [result, setResult] = useState<SolveResult | null>(null)
  const [windows, setWindows] = useState<WindowRow[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [explainOpen, setExplainOpen] = useState(false)
  const [explainPick, setExplainPick] = useState<string>('')
  const [explanation, setExplanation] = useState<Explanation | null>(null)
  const [unschedOpen, setUnschedOpen] = useState(false)
  const [publishing, setPublishing] = useState(false)
  const [published, setPublished] = useState<string | null>(null)

  useEffect(() => { api.windows().then(setWindows) }, [])

  async function run(nextStrict = strict, nextUrgency = urgency) {
    setLoading(true)
    setError(null)
    try {
      const r = await api.solve(nextStrict, nextUrgency)
      setResult(r)
      const allIds = [...r.blocks.map((b) => b.request), ...r.unscheduled.map((u) => u.id)]
      setExplainPick((prev) => (allIds.includes(prev) ? prev : allIds[0] ?? ''))
    } catch (e: any) {
      setError(e.message)
      setResult(null)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { run() }, [])

  useEffect(() => {
    if (!explainOpen || !explainPick) return
    api.explain(explainPick, strict, urgency).then(setExplanation)
  }, [explainOpen, explainPick, strict, urgency, result])

  async function defer(rid: string) {
    await api.defer(rid)
    onChanged()
    run()
  }

  async function publish() {
    setPublishing(true)
    try {
      const { id } = await api.createPlan(strict, urgency)
      await api.publish(id)
      setPublished(`Published as plan #${id}. Departments can now see it.`)
      onChanged()
      setTimeout(() => setPublished(null), 4000)
    } finally {
      setPublishing(false)
    }
  }

  const requestOptions = result
    ? [
        ...result.blocks.map((b) => ({ id: b.request, label: `${b.request} — ${b.title}` })),
        ...result.unscheduled.map((u) => ({ id: u.id, label: `${u.id} — ${u.title}` })),
      ]
    : []

  return (
    <div className="mx-auto max-w-5xl px-8 py-10">
      <h1 className="text-[28px] font-extrabold tracking-tight text-[var(--ink)]">Plan the corridor</h1>
      <p className="mt-1 text-[var(--ink-soft)]">
        {sections.length} sections · {windows.length} traffic-free windows
      </p>

      <div className="mt-7 flex items-center gap-8 rounded-xl border border-slate-200 bg-white px-6 py-5">
        <div className="flex-1">
          <div className="mb-1.5 flex justify-between text-xs font-semibold text-[var(--ink-soft)]">
            <span>◀ protect service</span>
            <span>clear urgent ▶</span>
          </div>
          <input
            type="range" min={0} max={1} step={0.05} value={urgency}
            onChange={(e) => { const v = Number(e.target.value); setUrgency(v); run(strict, v) }}
            className="w-full accent-[var(--navy)]"
          />
        </div>
        <label className="flex flex-none items-center gap-2.5 text-sm font-semibold text-[var(--ink)]">
          <input
            type="checkbox" checked={strict}
            onChange={(e) => { setStrict(e.target.checked); run(e.target.checked, urgency) }}
            className="h-4 w-4 accent-[var(--navy)]"
          />
          Every request is mandatory
        </label>
      </div>

      {loading && (
        <div className="mt-8 flex items-center gap-2 text-sm text-[var(--ink-soft)]">
          <Loader2 size={16} className="animate-spin" /> Solving…
        </div>
      )}
      {error && (
        <div className="mt-8 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800">
          The solver could not run: {error}
        </div>
      )}

      {!loading && result && !result.ok && (
        <div className="mt-8">
          <div className="grid grid-cols-3 gap-4">
            <Metric label="Result" value="No valid plan" tone="red" />
            <Metric label="Requests in conflict" value={String(result.conflict.length)} />
            <Metric label="Proved in" value={`${result.solveTimeMs.toFixed(0)} ms`} />
          </div>
          <div className="mt-5 rounded-xl border border-red-200 bg-red-50 px-5 py-4">
            <div className="flex items-center gap-2 font-bold text-red-800">
              <AlertOctagon size={17} /> These requests cannot coexist.
            </div>
            <p className="mt-1.5 text-sm text-red-900">{result.conflictText}</p>
          </div>
          <p className="mt-2 text-sm text-[var(--ink-faint)]">
            This set is irreducible — deferring any one of them makes the rest solvable.
          </p>
          <div className="mt-4 overflow-hidden rounded-xl border border-slate-200 bg-white">
            {result.conflict.map((r, i) => (
              <div key={r.id} className={`grid grid-cols-[64px_1fr_1fr_auto_auto] items-center gap-4 px-5 py-3.5 ${i > 0 ? 'border-t border-slate-100' : ''}`}>
                <span className="mono text-sm font-bold">{r.id}</span>
                <span className="text-sm">{r.title}</span>
                <span className="text-xs text-[var(--ink-faint)]">{r.deptName} · {r.sectionName}</span>
                <span className="mono text-xs text-[var(--ink-faint)]">{r.duration} min · P{r.priority}</span>
                <button
                  onClick={() => defer(r.id)}
                  className="rounded-lg border border-slate-300 px-3 py-1.5 text-xs font-semibold hover:bg-slate-50"
                >
                  Defer
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {!loading && result && result.ok && (
        <div className="mt-8">
          <div className="grid grid-cols-4 gap-4">
            <Metric label="Result" value={result.provenOptimal ? 'Proven optimal' : 'Feasible'} tone="green" />
            <Metric label="Blocks scheduled" value={`${result.blocks.length} / ${result.requestCount}`} />
            <Metric label="Solved in" value={`${result.solveTimeMs.toFixed(0)} ms`} />
            <Metric label="Rule violations" value={String(result.violations.length)} tone={result.violations.length ? 'red' : undefined} />
          </div>

          <div className="mt-5">
            <Gantt sections={sections} windows={windows} blocks={result.blocks} days={result.days} />
          </div>

          {result.violations.length > 0 ? (
            <div className="mt-5 rounded-xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-900">
              <span className="font-bold">Verification failed.</span> {result.violations.join(' · ')}
            </div>
          ) : (
            <div className="mt-5 flex items-start gap-2.5 rounded-xl border border-emerald-200 bg-emerald-50 px-5 py-4 text-sm text-emerald-900">
              <CheckCircle2 size={18} className="mt-0.5 flex-none text-emerald-600" />
              <span>
                <b>Independently verified.</b> All {result.blocks.length} blocks re-checked against the rules from
                scratch: no section double-booked, every block inside a traffic-free window, no deadline missed,
                crew limits respected.
              </span>
            </div>
          )}

          <div className="mt-5 rounded-xl border border-slate-200 bg-white">
            <button
              onClick={() => setExplainOpen((v) => !v)}
              className="flex w-full items-center justify-between px-5 py-3.5 text-sm font-semibold text-[var(--ink)]"
            >
              <span className="flex items-center gap-2"><Sparkles size={15} /> Explain a block</span>
              <ChevronDown size={16} className={`transition-transform ${explainOpen ? 'rotate-180' : ''}`} />
            </button>
            {explainOpen && (
              <div className="border-t border-slate-100 px-5 py-5">
                <select
                  value={explainPick} onChange={(e) => setExplainPick(e.target.value)}
                  className="w-full max-w-lg rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:border-[var(--navy)]"
                >
                  {requestOptions.map((o) => <option key={o.id} value={o.id}>{o.label}</option>)}
                </select>
                {explanation && (
                  <div className="mt-4">
                    <div className={`rounded-lg px-4 py-2.5 text-sm font-bold ${explanation.scheduled ? 'bg-emerald-50 text-emerald-900' : 'bg-red-50 text-red-900'}`}>
                      {explanation.headline}
                    </div>
                    <ul className="mt-3 list-disc space-y-1.5 pl-5 text-sm text-[var(--ink)]">
                      {explanation.reasons.map((r, i) => <li key={i}>{r}</li>)}
                    </ul>
                    {explanation.alternatives.length > 0 && (
                      <div className="mt-4 overflow-hidden rounded-lg border border-slate-200">
                        <table className="w-full text-sm">
                          <thead className="bg-slate-50 text-xs uppercase text-[var(--ink-faint)]">
                            <tr><th className="px-3 py-2 text-left">Window</th><th className="px-3 py-2 text-left">Day</th><th className="px-3 py-2 text-left">Time</th><th className="px-3 py-2 text-left">Verdict</th><th className="px-3 py-2 text-left">Why</th></tr>
                          </thead>
                          <tbody>
                            {explanation.alternatives.map((a) => (
                              <tr key={a.window} className="border-t border-slate-100">
                                <td className="mono px-3 py-2">{a.window}</td>
                                <td className="mono px-3 py-2">{a.day}</td>
                                <td className="mono px-3 py-2">{a.span}</td>
                                <td className="px-3 py-2">{a.ok ? '✓ OK' : '✗ ruled out'}</td>
                                <td className="px-3 py-2 text-[var(--ink-soft)]">{a.why}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>

          {published && (
            <div className="mt-5 rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-2.5 text-sm font-medium text-emerald-800">
              {published}
            </div>
          )}
          <button
            onClick={publish} disabled={publishing}
            className="mt-5 flex items-center gap-2 rounded-lg bg-[var(--navy)] px-5 py-2.5 text-sm font-semibold text-white transition-opacity hover:opacity-90 disabled:opacity-60"
          >
            <Rocket size={15} /> {publishing ? 'Publishing…' : 'Publish as the block order'}
          </button>

          {result.unscheduled.length > 0 && (
            <div className="mt-6 rounded-xl border border-slate-200 bg-white">
              <button
                onClick={() => setUnschedOpen((v) => !v)}
                className="flex w-full items-center justify-between px-5 py-3.5 text-sm font-semibold text-[var(--ink)]"
              >
                Not scheduled ({result.unscheduled.length})
                <ChevronDown size={16} className={`transition-transform ${unschedOpen ? 'rotate-180' : ''}`} />
              </button>
              {unschedOpen && (
                <div className="border-t border-slate-100 px-5 py-4 text-sm">
                  <p className="mb-3 text-[var(--ink-faint)]">
                    The solver kept the highest-value work and dropped what could not fit. Switch on "every request
                    is mandatory" to see exactly why.
                  </p>
                  {result.unscheduled.map((r) => (
                    <div key={r.id} className="py-1">
                      <span className="mono font-semibold">{r.id}</span> — {r.title} · {r.sectionName} ·{' '}
                      {r.duration} min · P{r.priority}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function Metric({ label, value, tone }: { label: string; value: string; tone?: 'green' | 'red' }) {
  const color = tone === 'green' ? 'text-emerald-700' : tone === 'red' ? 'text-red-700' : 'text-[var(--ink)]'
  return (
    <div className="rounded-xl border border-slate-200 bg-white px-4 py-3">
      <div className="text-xs font-medium text-[var(--ink-faint)]">{label}</div>
      <div className={`mono mt-0.5 text-xl font-bold ${color}`}>{value}</div>
    </div>
  )
}
