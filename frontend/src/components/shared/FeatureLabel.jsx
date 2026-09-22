function FeatureLabel({ label, open, onToggle, compact = false }) {
  return (
    <button
      type="button"
      onClick={onToggle}
      aria-expanded={open}
      className={`group inline-flex cursor-pointer items-start gap-1.5 border-none bg-transparent p-0 text-left font-sans text-text-muted ${
        compact ? 'text-[13px]' : 'text-sm'
      }`}
    >
      <span className="leading-tight">{label}</span>
      <span
        aria-hidden="true"
        className={`mt-0.5 shrink-0 text-[11px] leading-none transition-colors group-hover:text-cyan ${
          open ? 'text-cyan' : 'text-text-dim'
        }`}
      >
        ⓘ
      </span>
    </button>
  )
}

export default FeatureLabel
