import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ReferenceLine, ResponsiveContainer, Cell,
} from 'recharts'

const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload?.length) return null
  const d = payload[0].payload
  return (
    <div className="bg-ink-800 border border-ink-600 rounded-lg px-3 py-2 text-xs">
      <p className="text-white font-medium">{d.feature}</p>
      <p className={d.value > 0 ? 'text-risk-high' : 'text-risk-low'}>
        SHAP: {d.value > 0 ? '+' : ''}{d.value.toFixed(4)}
      </p>
      <p className="text-white/40">{d.direction}</p>
    </div>
  )
}

export default function ShapChart({ prediction }) {
  if (!prediction) return null

  const data = Object.entries(prediction.shap_values)
    .map(([feature, value]) => ({
      feature,
      value,
      direction: value > 0 ? 'increases risk' : 'reduces risk',
    }))
    .sort((a, b) => Math.abs(b.value) - Math.abs(a.value))
    .slice(0, 8)

  return (
    <div className="card fade-up space-y-4">
      <div>
        <h2 className="text-base font-medium text-white">SHAP feature impact</h2>
        <p className="text-xs text-white/40 mt-0.5">
          Positive values increase default risk · negative values reduce it
        </p>
      </div>

      <ResponsiveContainer width="100%" height={260}>
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 0, right: 16, left: 0, bottom: 0 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#2a2a3d" horizontal={false} />
          <XAxis
            type="number"
            tick={{ fill: 'rgba(255,255,255,0.4)', fontSize: 11 }}
            axisLine={{ stroke: '#2a2a3d' }}
            tickLine={false}
          />
          <YAxis
            type="category"
            dataKey="feature"
            width={130}
            tick={{ fill: 'rgba(255,255,255,0.6)', fontSize: 11 }}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255,255,255,0.03)' }} />
          <ReferenceLine x={0} stroke="#3d3d5c" strokeWidth={1} />
          <Bar dataKey="value" radius={[0, 4, 4, 0]}>
            {data.map((entry, i) => (
              <Cell
                key={i}
                fill={entry.value > 0 ? '#ef4444' : '#22c55e'}
                fillOpacity={0.85}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
