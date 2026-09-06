import { CheckCircle2, Clock, ListTodo, Route, Zap } from 'lucide-react'
import { useEffect, useState } from 'react'
import { api } from '../api'
import { StatCard } from '../components/ui/StatCard'
import { StatCardSkeleton } from '../components/ui/Skeleton'
import type { Meta, RequestRow, SolveResult } from '../types'

export function DepartmentDashboard({ meta }: { meta: Meta }) {
  const [rows, setRows] = useState<RequestRow[] | null>(null)

  useEffect(() => { api.requests().then(setRows) }, [])

  const counts = rows
    ? {
        pending: rows.filter((r) => r.status === 'pending').length,
        planned: rows.filter((r) => r.status === 'planned').length,
        deferred: rows.filter((r) => r.status === 'deferred').length,
      }
    : null

  return (
    <div className="grid grid-cols-4 gap-4">
      {!rows ? (
        Array.from({ length: 4 }).map((_, i) => <StatCardSkeleton key={i} />)
      ) : (
        <>
          <StatCard icon={ListTodo} color="var(--color-accent)" label="My requests" value={rows.length} subtitle="submitted to this corridor" />
          <StatCard icon={Clock} color="var(--color-accent-amber)" label="Pending" value={counts!.pending} subtitle="awaiting the controller" />
          <StatCard icon={CheckCircle2} color="var(--color-accent-green)" label="Planned" value={counts!.planned} subtitle="in the live block order" />
          <StatCard icon={Route} color="var(--color-accent-purple)" label="Deferred" value={counts!.deferred} subtitle="dropped to resolve a conflict" />
        </>
      )}
      <div className="col-span-4 mt-1 rounded-xl border border-[var(--color-border)] bg-[var(--color-surface-elevated)] p-5 text-sm text-[var(--color-text-secondary)]">
        This corridor spans <b className="text-[var(--color-text-primary)]">{meta.sectionCount} sections</b> over a{' '}
        <b className="text-[var(--color-text-primary)]">{meta.days}-day</b> planning horizon.{' '}
        {meta.pendingCount} request{meta.pendingCount === 1 ? '' : 's'} across all departments are currently pending.
      </div>
    </div>
  )
}

export function ControllerDashboard({ meta }: { meta: Meta }) {
  const [solve, setSolve] = useState<SolveResult | null>(null)

  useEffect(() => { api.solve(false, 0.5).then(setSolve).catch(() => setSolve(null)) }, [])

  const publishedBlocks = meta.published ? undefined : 0

  return (
    <div className="grid grid-cols-4 gap-4">
      <StatCard icon={Route} color="var(--color-accent)" label="Sections" value={meta.sectionCount} subtitle={`${meta.windowCount} traffic-free windows`} />
      <StatCard icon={Clock} color="var(--color-accent-amber)" label="Pending requests" value={meta.pendingCount} subtitle="across all departments" />
      <StatCard
        icon={CheckCircle2} color="var(--color-accent-green)" label="Live block order"
        value={meta.published ? `plan #${meta.published.id}` : (publishedBlocks ?? 0)}
        subtitle={meta.published ? 'currently published' : 'none published yet'}
      />
      {!solve ? <StatCardSkeleton /> : (
        <StatCard
          icon={Zap} color={solve.ok ? 'var(--color-accent-green)' : 'var(--color-accent-red)'}
          label="Last solve" value={solve.ok ? `${solve.blocks.length}/${solve.requestCount}` : 'infeasible'}
          subtitle={solve.ok ? `${solve.solveTimeMs.toFixed(0)} ms · ${solve.violations.length} violations` : `${solve.conflict.length} in conflict`}
        />
      )}
    </div>
  )
}
