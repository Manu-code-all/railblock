import type { Block, Section, WindowRow } from '../types'
import { DEPT_COLOR } from '../types'

const DAY = 1440
const ROW_H = 46
const HEAD_H = 28
const LABEL_W = 168
const PX_PER_MIN = 0.09

interface Props {
  sections: Section[]
  windows: WindowRow[]
  blocks: Block[]
  days: number
}

export function Gantt({ sections, windows, blocks, days }: Props) {
  const width = LABEL_W + days * DAY * PX_PER_MIN
  const height = HEAD_H + sections.length * ROW_H + 8
  const x = (m: number) => LABEL_W + m * PX_PER_MIN

  return (
    <div className="overflow-x-auto rounded-[12px] border border-[var(--hairline)] bg-[var(--surface-1)]">
      <svg
        viewBox={`0 0 ${width} ${height}`}
        style={{ minWidth: width }}
        role="img"
        aria-label={`Gantt chart of ${blocks.length} scheduled blocks across ${sections.length} sections over ${days} days`}
      >
        {/* day gridlines + labels */}
        {Array.from({ length: days + 1 }).map((_, d) => (
          <g key={d}>
            <line
              x1={x(d * DAY)} x2={x(d * DAY)}
              y1={HEAD_H} y2={height - 4}
              stroke="#e4e4e7" strokeWidth={1}
            />
            {d < days && (
              <text
                x={x(d * DAY) + 4} y={16}
                fontSize={10.5} fontFamily="IBM Plex Mono" fill="#9a9ca1"
              >
                Day {d}
              </text>
            )}
          </g>
        ))}

        {/* rows */}
        {sections.map((s, i) => {
          const y = HEAD_H + i * ROW_H
          const rowWindows = windows.filter((w) => w.section === s.id)
          const rowBlocks = blocks.filter((b) => b.section === s.id)
          return (
            <g key={s.id}>
              <text
                x={0} y={y + ROW_H / 2 + 4}
                fontSize={12} fontWeight={600} fill="#17181a"
              >
                {s.name.length > 22 ? s.name.slice(0, 21) + '…' : s.name}
              </text>
              <line x1={0} x2={width} y1={y + ROW_H} y2={y + ROW_H} stroke="#eeeef0" />

              {rowWindows.map((w) => (
                <rect
                  key={w.id}
                  x={x(w.start)} y={y + 6}
                  width={Math.max(1, (w.end - w.start) * PX_PER_MIN)}
                  height={ROW_H - 12}
                  rx={4}
                  fill={w.disruption ? '#FBF3E4' : '#F2F5F9'}
                />
              ))}

              {rowBlocks.map((b) => {
                const color = DEPT_COLOR[b.dept] ?? '#64748B'
                const w = Math.max(2, (b.end - b.start) * PX_PER_MIN)
                return (
                  <g key={b.request}>
                    <rect
                      x={x(b.start)} y={y + 6}
                      width={w} height={ROW_H - 12}
                      rx={5} fill={color}
                    />
                    {w > 34 && (
                      <text
                        x={x(b.start) + 6} y={y + ROW_H / 2 + 4}
                        fontSize={10.5} fontWeight={600} fill="white"
                        fontFamily="IBM Plex Mono"
                      >
                        {b.request}
                      </text>
                    )}
                  </g>
                )
              })}
            </g>
          )
        })}
      </svg>
    </div>
  )
}
