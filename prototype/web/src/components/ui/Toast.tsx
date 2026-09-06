import { AlertTriangle, CheckCircle2, RotateCcw, X, XCircle } from 'lucide-react'
import { createContext, useCallback, useContext, useState } from 'react'

type ToastKind = 'success' | 'warning' | 'error'

interface ToastItem {
  id: number
  kind: ToastKind
  message: string
  onRetry?: () => void
}

interface ToastContextValue {
  push: (kind: ToastKind, message: string, onRetry?: () => void) => void
}

const ToastContext = createContext<ToastContextValue | null>(null)

export function useToast() {
  const ctx = useContext(ToastContext)
  if (!ctx) throw new Error('useToast must be used inside ToastProvider')
  return {
    success: (message: string) => ctx.push('success', message),
    warning: (message: string) => ctx.push('warning', message),
    error: (message: string, onRetry?: () => void) => ctx.push('error', message, onRetry),
  }
}

const STYLE: Record<ToastKind, { bg: string; fg: string; icon: typeof CheckCircle2 }> = {
  success: { bg: '#ecfdf5', fg: 'var(--color-accent-green)', icon: CheckCircle2 },
  warning: { bg: '#fffbeb', fg: 'var(--color-accent-amber)', icon: AlertTriangle },
  error: { bg: '#fef2f2', fg: 'var(--color-accent-red)', icon: XCircle },
}

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [items, setItems] = useState<ToastItem[]>([])

  const dismiss = useCallback((id: number) => {
    setItems((prev) => prev.filter((t) => t.id !== id))
  }, [])

  const push = useCallback((kind: ToastKind, message: string, onRetry?: () => void) => {
    const id = Date.now() + Math.random()
    setItems((prev) => [...prev, { id, kind, message, onRetry }])
    if (kind === 'success') {
      setTimeout(() => dismiss(id), 3000)
    }
  }, [dismiss])

  return (
    <ToastContext.Provider value={{ push }}>
      {children}
      <div className="pointer-events-none fixed bottom-5 right-5 z-50 flex flex-col gap-2">
        {items.map((t) => {
          const s = STYLE[t.kind]
          const Icon = s.icon
          return (
            <div
              key={t.id}
              className="pointer-events-auto flex items-start gap-2.5 rounded-lg border border-black/5 px-4 py-3 text-sm shadow-[var(--shadow-lg)] animate-[fade-up_0.15s_ease-out]"
              style={{ background: s.bg, color: s.fg, minWidth: 260, maxWidth: 360 }}
              role="status"
            >
              <Icon size={17} className="mt-0.5 flex-none" />
              <span className="flex-1 font-medium">{t.message}</span>
              {t.onRetry && (
                <button onClick={t.onRetry} className="flex items-center gap-1 rounded-md bg-white/60 px-2 py-1 text-xs font-semibold hover:bg-white">
                  <RotateCcw size={12} /> Retry
                </button>
              )}
              <button onClick={() => dismiss(t.id)} aria-label="Dismiss" className="flex-none opacity-60 hover:opacity-100">
                <X size={14} />
              </button>
            </div>
          )
        })}
      </div>
    </ToastContext.Provider>
  )
}
