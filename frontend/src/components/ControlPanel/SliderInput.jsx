import { useState } from 'react'
import FeatureLabel from '../shared/FeatureLabel'
import DefinitionPanel from '../shared/DefinitionPanel'
import { FEATURE_DEFINITIONS } from '../../data/featureDefinitions'

function SliderInput({ featureKey, min, max, value, onChange, hovered, onHover }) {
  const [infoOpen, setInfoOpen] = useState(false)
  const { label, text } = FEATURE_DEFINITIONS[featureKey]
  const pct = ((value - min) / (max - min)) * 100

  return (
    <div
      className={`-mx-2 mb-6 rounded-lg px-2 py-1 transition-colors ${hovered ? 'bg-cyan-950/10' : ''}`}
      onMouseEnter={() => onHover(featureKey)}
      onMouseLeave={() => onHover(null)}
    >
      <div className="mb-2 flex items-start justify-between">
        <FeatureLabel label={label} open={infoOpen} onToggle={() => setInfoOpen((o) => !o)} />
        <span className="font-mono text-sm font-bold text-text-primary">{value}</span>
      </div>
      <DefinitionPanel open={infoOpen} text={text} />
      <input
        type="range"
        min={min}
        max={max}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        style={{
          background: `linear-gradient(to right, #00f2fe 0%, #00f2fe ${pct}%, var(--color-grid-line) ${pct}%, var(--color-grid-line) 100%)`,
        }}
        className="h-1 w-full cursor-pointer appearance-none rounded-full outline-none
          [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:cursor-pointer
          [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:rounded-full
          [&::-webkit-slider-thumb]:bg-cyan [&::-webkit-slider-thumb]:shadow-[0_0_0_4px_rgba(0,242,254,0.3)]
          [&::-webkit-slider-thumb]:transition-shadow hover:[&::-webkit-slider-thumb]:shadow-[0_0_0_8px_rgba(0,242,254,0.3)]
          [&::-moz-range-thumb]:h-4 [&::-moz-range-thumb]:w-4 [&::-moz-range-thumb]:cursor-pointer
          [&::-moz-range-thumb]:rounded-full [&::-moz-range-thumb]:border-0 [&::-moz-range-thumb]:bg-cyan
          [&::-moz-range-thumb]:shadow-[0_0_0_4px_rgba(0,242,254,0.3)]"
      />
    </div>
  )
}

export default SliderInput
