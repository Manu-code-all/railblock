import { AnimatePresence, motion } from 'framer-motion'
import { useEffect, useState } from 'react'
import { api } from './api'
import { ROLES, Sidebar } from './components/Sidebar'
import type { Dept, Meta } from './types'
import { ActivityLog } from './views/ActivityLog'
import { BlockOrders } from './views/BlockOrders'
import { ControllerView } from './views/ControllerView'
import { DepartmentView } from './views/DepartmentView'

const CONTROLLER_TABS = ['Plan the corridor', 'Block orders', 'Activity log'] as const

export default function App() {
  const [role, setRole] = useState('Engineering (P.Way)')
  const [meta, setMeta] = useState<Meta | null>(null)
  const [tab, setTab] = useState<typeof CONTROLLER_TABS[number]>('Plan the corridor')

  const refresh = () => { api.meta().then(setMeta) }
  useEffect(() => { refresh() }, [])

  const dept = ROLES.find((r) => r.label === role)?.dept ?? null

  if (!meta) {
    return <div className="flex h-screen items-center justify-center text-[var(--ink-soft)]">Loading…</div>
  }

  if (meta.sectionCount === 0) {
    return (
      <div className="flex h-screen items-center justify-center bg-[var(--bg)]">
        <div className="max-w-md rounded-xl border border-slate-200 bg-white px-8 py-8 text-center">
          <h1 className="text-xl font-extrabold text-[var(--ink)]">RailBlock</h1>
          <p className="mt-2 text-sm text-[var(--ink-soft)]">
            No corridor is loaded, so there is nothing to plan yet.
          </p>
          <code className="mono mt-4 block rounded-lg bg-slate-100 px-3 py-2 text-xs">
            python -m railblock.seed
          </code>
        </div>
      </div>
    )
  }

  return (
    <div className="flex h-screen">
      <Sidebar
        role={role} setRole={setRole}
        sectionCount={meta.sectionCount} days={meta.days}
        pendingCount={meta.pendingCount}
        publishedPlanId={meta.published?.id ?? null}
      />
      <main className="flex-1 overflow-y-auto">
        {dept ? (
          <DepartmentView
            key={dept} dept={dept as Dept} roleLabel={role}
            sections={meta.sections} days={meta.days} onChanged={refresh}
          />
        ) : (
          <>
            <div className="sticky top-0 z-10 border-b border-slate-200 bg-[var(--bg)]/90 px-8 backdrop-blur">
              <div className="mx-auto flex max-w-5xl gap-1">
                {CONTROLLER_TABS.map((t) => (
                  <button
                    key={t}
                    onClick={() => setTab(t)}
                    className={`relative px-3 py-3 text-sm font-semibold transition-colors ${
                      tab === t ? 'text-[var(--navy)]' : 'text-[var(--ink-faint)] hover:text-[var(--ink-soft)]'
                    }`}
                  >
                    {t}
                    {tab === t && (
                      <motion.div layoutId="tab-underline" className="absolute inset-x-0 -bottom-px h-0.5 bg-[var(--navy)]" />
                    )}
                  </button>
                ))}
              </div>
            </div>
            <AnimatePresence mode="wait">
              <motion.div
                key={tab}
                initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
                transition={{ duration: 0.15 }}
              >
                {tab === 'Plan the corridor' && <ControllerView sections={meta.sections} onChanged={refresh} />}
                {tab === 'Block orders' && <BlockOrders />}
                {tab === 'Activity log' && <ActivityLog />}
              </motion.div>
            </AnimatePresence>
          </>
        )}
      </main>
    </div>
  )
}
