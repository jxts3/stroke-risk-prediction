const API_URL = 'https://stroke-risk-api.onrender.com/predict'

export async function predict(inputs) {
  const res = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(inputs),
  })

  if (!res.ok) {
    throw new Error(`Prediction failed (${res.status})`)
  }

  return res.json()
}
