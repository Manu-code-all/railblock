import { AnimatePresence, motion } from 'framer-motion'
import { BarChart3, Calendar, LayoutDashboard, Route, Settings as SettingsIcon } from 'lucide-react'
import { useEffect, useState } from 'react'
import { api } from './api'
import type { NavItem } from './components/ui/Sidebar'
import { Sidebar } from './components/ui/Sidebar'
import { Toolbar } from './components/ui/Toolbar'
import { ToastProvider } from './components/ui/Toast'
import type { Meta, Session } from './types'
import { ActivityLog } from './views/ActivityLog'
import { BlockOrders } from './views/BlockOrders'
import { ControllerDashboard, DepartmentDashboard } from './views/Dashboard'
import { Corridors } from './views/Corridors'
import { ControllerView } from './views/ControllerView'
import { DepartmentView } from './views/DepartmentView'
import { Login } from './views/Login'
import { Settings } from './views/Settings'

const PLANNER_TABS = ['Plan the corridor', 'Block orders'] as const

export default function App() {
  const [session, setSession] = useState<Session | null | 'checking'>('checking')
  const [meta, setMeta] = useState<Meta | null>(null)
  const [page, setPage] = useState('dashboard')
  const [plannerTab, setPlannerTab] = useState<typeof PLANNER_TABS[number]>('Plan the corridor')

  useEffect(() => {
    if (!api.isLoggedIn()) { setSession(null); return }
    api.me().then(setSession).catch(() => setSession(null))
  }, [])

  const refresh = () => { api.meta().then(setMeta) }
  useEffect(() => {
    if (session && session !== 'checking') refresh()
  }, [session])

  async function logout() {
    await api.logout()
    setSession(null)
    setMeta(null)
  }

  if (session === 'checking') {
    return <div className="flex h-screen items-center justify-center text-[var(--color-text-secondary)]">Loading…</div>
  }

  if (!session) {
    return (
      <ToastProvider>
        <Login onLoggedIn={setSession} />
      </ToastProvider>
    )
  }

  if (!meta) {
    return <div className="flex h-screen items-center justify-center text-[var(--color-text-secondary)]">Loading…</div>
  }

  if (meta.sectionCount === 0) {
    return (
      <div className="flex h-screen items-center justify-center bg-[var(--color-surface)]">
        <div className="max-w-md rounded-xl border border-[var(--color-border)] bg-[var(--color-surface-elevated)] px-8 py-8 text-center shadow-[var(--shadow-md)]">
          <h1 className="text-xl font-semibold text-[var(--color-text-primary)]">RailBlock</h1>
          <p className="mt-2 text-sm text-[var(--color-text-secondary)]">
            No corridor is loaded, so there is nothing to plan yet.
          </p>
          <code className="mono mt-4 block rounded-lg bg-[var(--color-surface)] px-3 py-2 text-xs">
            python -m railblock.seed
          </code>
        </div>
      </div>
    )
  }

  const isController = session.dept === null
  const navItems: NavItem[] = [
    { key: 'dashboard', label: 'Dashboard', icon: LayoutDashboard, group: 'Operations' },
    { key: 'corridors', label: 'Corridors', icon: Route, group: 'Operations' },
    { key: 'planner', label: 'Planner', icon: Calendar, group: 'Operations' },
    ...(isController ? [{ key: 'reports', label: 'Reports', icon: BarChart3, group: 'Admin' as const }] : []),
    { key: 'settings', label: 'Settings', icon: SettingsIcon, group: 'Admin' },
  ]

  const titles: Record<string, { title: string; breadcrumb: string }> = {
    dashboard: { title: 'Dashboard', breadcrumb: 'RailBlock / Overview' },
    corridors: { title: 'Corridors', breadcrumb: 'RailBlock / Corridors' },
    planner: { title: 'Corridor Planner', breadcrumb: 'RailBlock / Planner' },
    reports: { title: 'Reports', breadcrumb: 'RailBlock / Reports' },
    settings: { title: 'Settings', breadcrumb: 'RailBlock / Settings' },
  }

  return (
    <ToastProvider>
      <div className="flex h-screen">
        <Sidebar items={navItems} active={page} onSelect={setPage} user={session} onLogout={logout} />
        <div className="flex min-w-0 flex-1 flex-col">
          <Toolbar
            title={titles[page].title}
            breadcrumb={titles[page].breadcrumb}
            user={session}
            notificationCount={isController ? meta.pendingCount : 0}
            notificationLabel={`${meta.pendingCount} request(s) pending across all departments.`}
          />
          <main className="flex-1 overflow-y-auto bg-[var(--color-surface)] p-6">
            <AnimatePresence mode="wait">
              <motion.div
                key={page}
                initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
                transition={{ duration: 0.15 }}
              >
                {page === 'dashboard' && (
                  isController ? <ControllerDashboard meta={meta} /> : <DepartmentDashboard meta={meta} />
                )}
                {page === 'corridors' && <Corridors meta={meta} />}
                {page === 'planner' && (
                  isController ? (
                    <div>
                      <div className="mb-5 flex gap-1 border-b border-[var(--color-border)]">
                        {PLANNER_TABS.map((t) => (
                          <button
                            key={t}
                            onClick={() => setPlannerTab(t)}
                            className={`relative px-3 py-2.5 text-sm font-medium transition-colors ${
                              plannerTab === t ? 'text-[var(--color-text-primary)]' : 'text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)]'
                            }`}
                          >
                            {t}
                            {plannerTab === t && (
                              <motion.div layoutId="planner-tab-underline" className="absolute inset-x-0 -bottom-px h-0.5 bg-[var(--color-accent)]" />
                            )}
                          </button>
                        ))}
                      </div>
                      {plannerTab === 'Plan the corridor'
                        ? <ControllerView sections={meta.sections} onChanged={refresh} />
                        : <BlockOrders />}
                    </div>
                  ) : session.dept ? (
                    <DepartmentView
                      key={session.dept} dept={session.dept}
                      sections={meta.sections} days={meta.days} onChanged={refresh}
                    />
                  ) : null
                )}
                {page === 'reports' && isController && <ActivityLog />}
                {page === 'settings' && <Settings user={session} meta={meta} />}
              </motion.div>
            </AnimatePresence>
          </main>
        </div>
      </div>
    </ToastProvider>
  )
}
