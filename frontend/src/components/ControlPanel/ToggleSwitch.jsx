import { useState } from 'react'
import FeatureLabel from '../shared/FeatureLabel'
import DefinitionPanel from '../shared/DefinitionPanel'
import { FEATURE_DEFINITIONS } from '../../data/featureDefinitions'

function ToggleSwitch({ featureKey, checked, onChange, hovered, onHover }) {
  const [infoOpen, setInfoOpen] = useState(false)
  const { label, text } = FEATURE_DEFINITIONS[featureKey]

  return (
    <div
      className={`-mx-2 rounded-lg px-2 py-1 transition-colors ${hovered ? 'bg-cyan-950/10' : ''}`}
      onMouseEnter={() => onHover(featureKey)}
      onMouseLeave={() => onHover(null)}
    >
      <div className="flex items-center justify-between">
        <FeatureLabel label={label} open={infoOpen} onToggle={() => setInfoOpen((o) => !o)} />
        <button
          type="button"
          role="switch"
          aria-checked={checked}
          aria-label={label}
          onClick={() => onChange(!checked)}
          className={`relative h-[22px] w-10 cursor-pointer rounded-full border-none transition-colors ${
            checked ? 'bg-[#00F2FE] shadow-[0_0_10px_rgba(0,242,254,0.5)]' : 'bg-slate-800'
          }`}
        >
          <span
            className={`absolute top-[3px] left-[3px] h-4 w-4 rounded-full bg-text-primary transition-transform ${
              checked ? 'translate-x-[18px]' : ''
            }`}
          />
        </button>
      </div>
      <DefinitionPanel open={infoOpen} text={text} />
    </div>
  )
}

export default ToggleSwitch
