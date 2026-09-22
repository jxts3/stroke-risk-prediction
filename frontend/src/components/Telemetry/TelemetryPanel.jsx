import RiskGauge from './RiskGauge'
import ShapBarChart from './ShapBarChart'

function TelemetryPanel({ result, loading, error, hoveredFeature }) {
  return (
    <section className="animate-slide-right rounded-2xl border border-white/5 border-t-2 border-l-2 border-t-cyan-500/40 border-l-cyan-500/40 bg-card p-7 backdrop-blur-md">
      <div className="mb-5 flex items-center justify-between">
        <h2 className="font-heading text-base font-bold tracking-widest text-cyan-400/90 uppercase">
          Diagnostic telemetry
        </h2>
        <button
          type="button"
          onClick={() => window.print()}
          className="cursor-pointer rounded-md border border-cyan-500/30 bg-white/[0.03] px-2.5 py-1.5 font-mono
            text-[11px] font-bold text-cyan-400/90 transition-all hover:border-cyan-400 hover:bg-cyan-950/30"
        >
          [ EXPORT ASSESSMENT ]
        </button>
      </div>
      {error && <p className="mb-4 text-[13px] text-danger">Prediction unavailable — {error}</p>}
      <RiskGauge percentage={result?.risk_percentage} label={result?.risk_label} loading={loading} />
      <p className="mt-5 mb-5 text-center text-[12.5px] text-text-dim">
        How much each factor pushed this prediction up or down.
      </p>
      <ShapBarChart values={result?.shap_values ?? []} hoveredFeature={hoveredFeature} />
    </section>
  )
}

export default TelemetryPanel
