import { ShieldCheck, ShieldAlert, ShieldX } from 'lucide-react'

const BAND_CONFIG = {
  'Low risk':       { color: 'text-risk-low',    bg: 'bg-risk-low/10',    border: 'border-risk-low/30',    Icon: ShieldCheck },
  'Medium risk':    { color: 'text-risk-medium',  bg: 'bg-risk-medium/10', border: 'border-risk-medium/30', Icon: ShieldAlert  },
  'High risk':      { color: 'text-risk-high',    bg: 'bg-risk-high/10',   border: 'border-risk-high/30',   Icon: ShieldX      },
  'Very high risk': { color: 'text-risk-vhigh',   bg: 'bg-risk-vhigh/10',  border: 'border-risk-vhigh/30',  Icon: ShieldX      },
}

function GaugeArc({ prob }) {
  const pct   = Math.min(Math.max(prob, 0), 1)
  const angle = pct * 180 - 90
  const r     = 70
  const cx    = 100
  const cy    = 100

  const toXY = (deg) => {
    const rad = (deg * Math.PI) / 180
    return { x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad) }
  }

  const start = toXY(-180)
  const end   = toXY(0)
  const cur   = toXY(angle - 90)

  const color =
    pct < 0.15 ? '#22c55e' :
    pct < 0.35 ? '#f59e0b' :
    pct < 0.60 ? '#ef4444' : '#dc2626'

  return (
    <svg viewBox="0 0 200 110" className="w-48">
      <path
        d={`M ${start.x} ${start.y} A ${r} ${r} 0 0 1 ${end.x} ${end.y}`}
        fill="none" stroke="#1c1c28" strokeWidth="12" strokeLinecap="round"
      />
      <path
        d={`M ${start.x} ${start.y} A ${r} ${r} 0 0 1 ${cur.x} ${cur.y}`}
        fill="none" stroke={color} strokeWidth="12" strokeLinecap="round"
      />
      <text x={cx} y={cy - 10} textAnchor="middle" fill="white" fontSize="22" fontWeight="600" fontFamily="DM Sans">
        {(prob * 100).toFixed(1)}%
      </text>
      <text x={cx} y={cy + 12} textAnchor="middle" fill="rgba(255,255,255,0.4)" fontSize="10" fontFamily="DM Sans">
        default probability
      </text>
    </svg>
  )
}

export default function ResultsCard({ prediction }) {
  if (!prediction) return null

  const cfg = BAND_CONFIG[prediction.risk_band] || BAND_CONFIG['High risk']
  const { Icon } = cfg

  return (
    <div className="card fade-up space-y-5">
      <h2 className="text-base font-medium text-white">Assessment result</h2>

      <div className="flex items-center justify-between">
        <GaugeArc prob={prediction.default_probability} />

        <div className="flex flex-col gap-3 items-end">
          <div className={`risk-badge border ${cfg.bg} ${cfg.color} ${cfg.border}`}>
            <Icon size={13} />
            {prediction.risk_band}
          </div>

          <div className={`text-2xl font-semibold tracking-tight ${
            prediction.decision === 'Approved' ? 'text-risk-low' : 'text-risk-high'
          }`}>
            {prediction.decision}
          </div>
        </div>
      </div>

      <div className="space-y-2">
        <p className="text-xs text-white/40 uppercase tracking-wider">Top risk factors</p>
        {prediction.top_factors.map((f, i) => (
          <div key={i} className="flex items-center justify-between text-sm">
            <span className="text-white/70">{f.feature}</span>
            <span className={`font-mono text-xs ${f.shap_value > 0 ? 'text-risk-high' : 'text-risk-low'}`}>
              {f.shap_value > 0 ? '+' : ''}{f.shap_value.toFixed(3)}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}
