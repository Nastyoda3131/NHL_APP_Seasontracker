import { useEffect, useState } from 'react'
import { getBackendHealth } from './api/client'
import './App.css'

function App() {
  const [backendStatus, setBackendStatus] = useState<string>('checking...')
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getBackendHealth()
      .then((data) => {
        setBackendStatus(data.status)
        setError(null)
      })
      .catch((err) => {
        setBackendStatus('unreachable')
        setError(err instanceof Error ? err.message : 'Unknown error')
      })
  }, [])

  return (
    <main className="app-shell">
      <section className="card">
        <p className="eyebrow">NHL Topscorer App</p>
        <h1>Seasontracker</h1>

        <div className="status-row">
          <span>Backend status</span>
          <strong>{backendStatus}</strong>
        </div>

        {error && <p className="error">{error}</p>}

        <p className="hint">
          Frontend und Backend sind verbunden. Nächster Schritt: Login und Team-Dashboard.
        </p>
      </section>
    </main>
  )
}

export default App