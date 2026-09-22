const RISK_COLORS = {
  Low: 'var(--color-safe)',
  Moderate: 'var(--color-moderate)',
  High: 'var(--color-danger)',
}

function RiskGauge({ percentage, label, loading }) {
  const pct = percentage ?? 0
  const size = 220
  const stroke = 16
  const r = (size - stroke) / 2
  const c = size / 2
  const circumference = 2 * Math.PI * r
  const offset = circumference * (1 - pct / 100)
  const color = RISK_COLORS[label] ?? 'var(--color-text-dim)'
  const glow = label === 'High' ? 'drop-shadow-[0_0_12px_rgba(255,59,48,0.5)]' : ''

  return (
    <div className={`relative mx-auto mb-2 flex w-[220px] justify-center ${glow}`}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} style={{ transform: 'rotate(-90deg)' }}>
        <circle fill="none" stroke="var(--color-grid-line)" cx={c} cy={c} r={r} strokeWidth={stroke} />
        <circle
          fill="none"
          strokeLinecap="round"
          cx={c}
          cy={c}
          r={r}
          strokeWidth={stroke}
          stroke={color}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          style={{ transition: 'stroke-dashoffset 0.6s cubic-bezier(.3,.9,.3,1), stroke 0.3s ease' }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="font-mono text-4xl font-bold" style={{ color }}>
          {loading ? '···' : `${pct.toFixed(0)}%`}
        </span>
        <span className="mt-1 text-[13px] text-text-muted capitalize">
          {loading ? 'Calculating' : `${label ?? '—'} risk`}
        </span>
      </div>
    </div>
  )
}

export default RiskGauge
