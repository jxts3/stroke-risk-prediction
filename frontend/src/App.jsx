import { useState } from 'react'
import Header from './components/Header'
import ProjectOverviewCard from './components/ProjectOverviewCard'
import ControlPanel from './components/ControlPanel/ControlPanel'
import TelemetryPanel from './components/Telemetry/TelemetryPanel'
import PrintableSummary from './components/PrintableSummary'
import usePredict from './hooks/usePredict'
import { DEFAULT_INPUTS } from './data/presets'

function App() {
  const [inputs, setInputs] = useState(DEFAULT_INPUTS)
  const [hoveredFeature, setHoveredFeature] = useState(null)
  const { result, loading, error } = usePredict(inputs)

  return (
    <>
      <div className="mx-auto max-w-[1080px] px-6 pt-12 pb-20 print:hidden">
        <Header />
        <ProjectOverviewCard />
        <main className="grid grid-cols-1 items-start gap-6 lg:grid-cols-2">
          <ControlPanel
            inputs={inputs}
            onChange={setInputs}
            hoveredFeature={hoveredFeature}
            onHoverFeature={setHoveredFeature}
          />
          <TelemetryPanel
            result={result}
            loading={loading}
            error={error}
            hoveredFeature={hoveredFeature}
          />
        </main>
      </div>
      <PrintableSummary inputs={inputs} result={result} />
    </>
  )
}

export default App
