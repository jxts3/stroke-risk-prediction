import { useState } from 'react'

function ProjectOverviewCard() {
  const [open, setOpen] = useState(false)

  return (
    <section className="animate-scale-in mb-6 rounded-2xl border border-white/5 bg-card px-7 py-5 backdrop-blur-md">
      <button
        type="button"
        className="flex w-full cursor-pointer items-center justify-between border-none bg-transparent p-0 font-sans text-[15px] font-semibold text-text-primary"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
      >
        <span className="font-heading text-base font-bold tracking-widest text-cyan-400/90 uppercase">
          About this project
        </span>
        <span className={`text-text-dim transition-transform duration-200 ${open ? 'rotate-180' : ''}`}>⌄</span>
      </button>
      {open && (
        <div className="mt-4 text-sm leading-relaxed text-text-muted">
          <p className="m-0">
            An interpretable machine learning tool that estimates stroke risk from a
            handful of clinical factors, and shows exactly what's driving each estimate.
          </p>
          <ul className="mt-3 list-disc pl-5">
            <li className="mb-1">Synthetic EHR cohort generated with Synthea</li>
            <li className="mb-1">Logistic regression model over six clinical features</li>
            <li className="mb-1">Live SHAP attribution for every prediction</li>
            <li className="mb-1">FastAPI backend + React / Vite frontend</li>
          </ul>
        </div>
      )}
    </section>
  )
}

export default ProjectOverviewCard
