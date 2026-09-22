import { DEFAULT_INPUTS, LOW_RISK_PRESET, HIGH_RISK_PRESET } from '../../data/presets'

function PresetButtons({ onApply }) {
  return (
    <div className="mb-6 flex gap-2.5">
      <button
        type="button"
        onClick={() => onApply(LOW_RISK_PRESET)}
        className="flex-1 cursor-pointer rounded-md border border-safe/30 bg-white/[0.03] px-3 py-2.5 text-[13px]
          font-semibold text-safe transition-all hover:border-safe hover:bg-safe/10 hover:shadow-[0_0_12px_rgba(16,185,129,0.25)]"
      >
        Low risk preset
      </button>
      <button
        type="button"
        onClick={() => onApply(HIGH_RISK_PRESET)}
        className="flex-1 cursor-pointer rounded-md border border-danger/30 bg-white/[0.03] px-3 py-2.5 text-[13px]
          font-semibold text-danger transition-all hover:border-danger hover:bg-danger/10 hover:shadow-[0_0_12px_rgba(255,59,48,0.25)]"
      >
        High risk preset
      </button>
      <button
        type="button"
        onClick={() => onApply(DEFAULT_INPUTS)}
        aria-label="Reset to baseline"
        title="Reset to baseline"
        className="flex cursor-pointer items-center justify-center rounded-md border border-cyan-500/30 bg-white/[0.03]
          px-3 py-2.5 text-[13px] font-semibold text-cyan-400/90 transition-all hover:border-cyan-400 hover:bg-cyan-950/30"
      >
        ↺
      </button>
    </div>
  )
}

export default PresetButtons
