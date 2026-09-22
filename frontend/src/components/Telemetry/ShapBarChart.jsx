import { useState } from 'react'
import FeatureLabel from '../shared/FeatureLabel'
import DefinitionPanel from '../shared/DefinitionPanel'
import { FEATURE_DEFINITIONS, SHAP_LABEL_TO_KEY } from '../../data/featureDefinitions'

function ShapRow({ feature, value, maxAbs, isHighlighted }) {
  const [infoOpen, setInfoOpen] = useState(false)
  const text = FEATURE_DEFINITIONS[SHAP_LABEL_TO_KEY[feature]]?.text
  const widthPct = Math.min(45, (Math.abs(value) / maxAbs) * 45)
  const isUp = value > 0

  return (
    <div
      className={`-mx-2 rounded-lg px-2 py-1 transition-all ${
        isHighlighted ? 'bg-cyan-950/10 ring-1 ring-cyan-400/50 shadow-[0_0_12px_rgba(34,211,238,0.25)]' : ''
      }`}
    >
      <div className="grid grid-cols-[130px_1fr_56px] items-center gap-2.5">
        <FeatureLabel label={feature} open={infoOpen} onToggle={() => setInfoOpen((o) => !o)} compact />
        <div className="relative h-1.5 rounded-full bg-grid-line">
          <div
            className={`absolute top-0 h-full rounded-full ${
              isUp
                ? 'left-1/2 bg-danger shadow-[0_0_6px_0_rgba(255,59,48,0.3)]'
                : 'right-1/2 bg-safe shadow-[0_0_6px_0_rgba(16,185,129,0.3)]'
            }`}
            style={{ width: `${widthPct}%`, transition: 'width 0.4s ease' }}
          />
        </div>
        <span className="text-right font-mono text-[12.5px] font-bold text-text-primary">
          {value >= 0 ? '+' : ''}
          {value.toFixed(2)}
        </span>
      </div>
      <DefinitionPanel open={infoOpen} text={text} />
    </div>
  )
}

function ShapBarChart({ values, hoveredFeature }) {
  const maxAbs = Math.max(1e-6, ...values.map((v) => Math.abs(v.value)))

  return (
    <div className="flex flex-col gap-3.5">
      {values.map((v) => (
        <ShapRow
          key={v.feature}
          feature={v.feature}
          value={v.value}
          maxAbs={maxAbs}
          isHighlighted={hoveredFeature !== null && SHAP_LABEL_TO_KEY[v.feature] === hoveredFeature}
        />
      ))}
    </div>
  )
}

export default ShapBarChart
