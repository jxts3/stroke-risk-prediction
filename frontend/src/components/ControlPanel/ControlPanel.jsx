import SliderInput from './SliderInput'
import ToggleSwitch from './ToggleSwitch'
import PresetButtons from './PresetButtons'

function ControlPanel({ inputs, onChange, hoveredFeature, onHoverFeature }) {
  const setField = (key) => (value) => onChange((prev) => ({ ...prev, [key]: value }))

  return (
    <section className="animate-slide-left rounded-2xl border border-white/5 border-t-2 border-l-2 border-t-cyan-500/40 border-l-cyan-500/40 bg-card p-7 backdrop-blur-md">
      <h2 className="mb-5 font-heading text-base font-bold tracking-widest text-cyan-400/90 uppercase">
        Input control panel
      </h2>

      <PresetButtons onApply={onChange} />

      <SliderInput
        featureKey="age"
        min={18}
        max={100}
        value={inputs.age}
        onChange={setField('age')}
        hovered={hoveredFeature === 'age'}
        onHover={onHoverFeature}
      />
      <SliderInput
        featureKey="n_conditions"
        min={0}
        max={30}
        value={inputs.n_conditions}
        onChange={setField('n_conditions')}
        hovered={hoveredFeature === 'n_conditions'}
        onHover={onHoverFeature}
      />
      <SliderInput
        featureKey="n_medications"
        min={0}
        max={30}
        value={inputs.n_medications}
        onChange={setField('n_medications')}
        hovered={hoveredFeature === 'n_medications'}
        onHover={onHoverFeature}
      />

      <div className="mt-1 flex flex-col gap-3.5">
        <ToggleSwitch
          featureKey="hypertension"
          checked={!!inputs.hypertension}
          onChange={(v) => setField('hypertension')(v ? 1 : 0)}
          hovered={hoveredFeature === 'hypertension'}
          onHover={onHoverFeature}
        />
        <ToggleSwitch
          featureKey="afib"
          checked={!!inputs.afib}
          onChange={(v) => setField('afib')(v ? 1 : 0)}
          hovered={hoveredFeature === 'afib'}
          onHover={onHoverFeature}
        />
        <ToggleSwitch
          featureKey="diabetes"
          checked={!!inputs.diabetes}
          onChange={(v) => setField('diabetes')(v ? 1 : 0)}
          hovered={hoveredFeature === 'diabetes'}
          onHover={onHoverFeature}
        />
      </div>
    </section>
  )
}

export default ControlPanel
