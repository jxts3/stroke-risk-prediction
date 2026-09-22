import { FEATURE_DEFINITIONS } from '../data/featureDefinitions'

function PrintableSummary({ inputs, result }) {
  const timestamp = new Date().toLocaleString()

  return (
    <div className="hidden bg-white p-8 text-black print:block">
      <h1 className="mb-1 text-2xl font-bold">Stroke Risk Predictor — Diagnostic Report</h1>
      <p className="mb-6 text-sm text-gray-600">
        Generated {timestamp} · Synthetic EHR data, portfolio project — not a clinical tool
      </p>

      <h2 className="mb-2 text-lg font-semibold">Patient inputs</h2>
      <table className="mb-6 w-full border-collapse text-sm">
        <tbody>
          <tr>
            <td className="border-b border-gray-300 py-1 pr-4">{FEATURE_DEFINITIONS.age.label}</td>
            <td className="border-b border-gray-300 py-1">{inputs.age}</td>
          </tr>
          <tr>
            <td className="border-b border-gray-300 py-1 pr-4">{FEATURE_DEFINITIONS.hypertension.label}</td>
            <td className="border-b border-gray-300 py-1">{inputs.hypertension ? 'Yes' : 'No'}</td>
          </tr>
          <tr>
            <td className="border-b border-gray-300 py-1 pr-4">{FEATURE_DEFINITIONS.afib.label}</td>
            <td className="border-b border-gray-300 py-1">{inputs.afib ? 'Yes' : 'No'}</td>
          </tr>
          <tr>
            <td className="border-b border-gray-300 py-1 pr-4">{FEATURE_DEFINITIONS.diabetes.label}</td>
            <td className="border-b border-gray-300 py-1">{inputs.diabetes ? 'Yes' : 'No'}</td>
          </tr>
          <tr>
            <td className="border-b border-gray-300 py-1 pr-4">{FEATURE_DEFINITIONS.n_conditions.label}</td>
            <td className="border-b border-gray-300 py-1">{inputs.n_conditions}</td>
          </tr>
          <tr>
            <td className="border-b border-gray-300 py-1 pr-4">{FEATURE_DEFINITIONS.n_medications.label}</td>
            <td className="border-b border-gray-300 py-1">{inputs.n_medications}</td>
          </tr>
        </tbody>
      </table>

      <h2 className="mb-2 text-lg font-semibold">Model result</h2>
      {result ? (
        <p className="mb-6 text-sm">
          Predicted stroke risk: <strong>{result.risk_percentage.toFixed(1)}%</strong> ({result.risk_label} risk)
        </p>
      ) : (
        <p className="mb-6 text-sm">No prediction available.</p>
      )}

      <h2 className="mb-2 text-lg font-semibold">SHAP attribution</h2>
      <table className="w-full border-collapse text-sm">
        <thead>
          <tr>
            <th className="border-b border-gray-400 py-1 text-left">Factor</th>
            <th className="border-b border-gray-400 py-1 text-right">Contribution</th>
          </tr>
        </thead>
        <tbody>
          {(result?.shap_values ?? []).map((v) => (
            <tr key={v.feature}>
              <td className="border-b border-gray-200 py-1">{v.feature}</td>
              <td className="border-b border-gray-200 py-1 text-right">
                {v.value >= 0 ? '+' : ''}
                {v.value.toFixed(2)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <p className="mt-8 text-xs text-gray-500">
        Model: logistic regression trained on synthetic EHR data (Synthea) · Explainability: SHAP LinearExplainer
      </p>
    </div>
  )
}

export default PrintableSummary
