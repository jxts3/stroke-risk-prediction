import { useEffect, useRef, useState } from 'react'
import { predict } from '../api/predict'

const DEBOUNCE_MS = 300

export default function usePredict(inputs) {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const timeoutRef = useRef(null)

  useEffect(() => {
    setLoading(true)
    setError(null)
    clearTimeout(timeoutRef.current)

    timeoutRef.current = setTimeout(() => {
      predict(inputs)
        .then((data) => {
          setResult(data)
          setLoading(false)
        })
        .catch((err) => {
          setError(err.message)
          setLoading(false)
        })
    }, DEBOUNCE_MS)

    return () => clearTimeout(timeoutRef.current)
  }, [inputs])

  return { result, loading, error }
}
