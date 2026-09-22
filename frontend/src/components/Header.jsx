function Header() {
  return (
    <header className="animate-slide-down mb-6 text-center">
      <div className="flex flex-wrap items-center justify-center gap-4">
        <h1 className="m-0 bg-gradient-to-r from-white via-slate-100 to-[#00F2FE] bg-clip-text font-display text-[42px] font-black tracking-wider text-transparent uppercase drop-shadow-[0_0_15px_rgba(0,242,254,0.3)]">
          Stroke Risk Predictor
        </h1>
        <span className="inline-flex items-center gap-2 text-xs font-semibold tracking-wider text-safe">
          <span className="animate-pulse-glow h-2 w-2 rounded-full bg-safe shadow-[0_0_8px_2px_rgba(16,185,129,0.3)]" />
          LIVE ENGINE
        </span>
      </div>
      <p className="mt-2 font-heading text-sm font-semibold tracking-widest text-slate-300">
        by <span className="text-[#00F2FE]">Jesse Igbide</span>
      </p>
      <p className="mt-1 font-mono text-[10px] text-slate-400">
        INFERENCE: ~12ms | MODEL: XGBoost + SHAP v2.4 | STATUS: ONLINE
      </p>
    </header>
  )
}

export default Header
