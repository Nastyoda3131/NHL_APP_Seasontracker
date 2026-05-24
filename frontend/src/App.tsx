import { useEffect, useMemo, useState } from 'react'
import { getTeamDashboard, type Player, type TeamDashboard } from './api/client'
import './App.css'

function formatUsd(value: string | number) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 0,
  }).format(Number(value))
}

function groupPlayersByPosition(players: Player[]) {
  return {
    G: players.filter((player) => player.position === 'G'),
    D: players.filter((player) => player.position === 'D'),
    F: players.filter((player) => player.position === 'F'),
  }
}

function App() {
  const [dashboard, setDashboard] = useState<TeamDashboard | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    getTeamDashboard()
      .then((data) => {
        setDashboard(data)
        setError(null)
      })
      .catch((err) => {
        setError(err instanceof Error ? err.message : 'Unknown error')
      })
      .finally(() => {
        setIsLoading(false)
      })
  }, [])

  const groupedPlayers = useMemo(() => {
    if (!dashboard) {
      return { G: [], D: [], F: [] }
    }

    return groupPlayersByPosition(dashboard.players)
  }, [dashboard])

  if (isLoading) {
    return (
      <main className="app-shell">
        <section className="card">
          <p className="eyebrow">NHL Topscorer App</p>
          <h1>Lade Team...</h1>
        </section>
      </main>
    )
  }

  if (error || !dashboard) {
    return (
      <main className="app-shell">
        <section className="card">
          <p className="eyebrow">NHL Topscorer App</p>
          <h1>Dashboard nicht verfügbar</h1>
          <p className="error">{error ?? 'Keine Teamdaten gefunden.'}</p>
          <p className="hint">
            Prüfe, ob das Backend läuft und ob POST /api/dev/seed bereits ausgeführt wurde.
          </p>
        </section>
      </main>
    )
  }

  return (
    <main className="app-shell">
      <section className="dashboard">
        <header className="hero-card">
          <p className="eyebrow">NHL Topscorer App</p>
          <h1>{dashboard.team_name}</h1>
          <p className="owner">Owner: {dashboard.owner_name}</p>

          <div className="summary-grid">
            <div className="summary-box">
              <span>Cash</span>
              <strong>{formatUsd(dashboard.cash_balance)}</strong>
            </div>
            <div className="summary-box">
              <span>Spieler</span>
              <strong>{dashboard.players.length}</strong>
            </div>
            <div className="summary-box">
              <span>Teamwert</span>
              <strong>
                {formatUsd(
                  dashboard.players.reduce((sum, player) => sum + Number(player.market_value), 0),
                )}
              </strong>
            </div>
          </div>
        </header>

        <section className="section-card">
          <h2>Kader</h2>

          <PlayerGroup title="Goalie" players={groupedPlayers.G} />
          <PlayerGroup title="Defensemen" players={groupedPlayers.D} />
          <PlayerGroup title="Forwards" players={groupedPlayers.F} />
        </section>

        <section className="section-card">
          <h2>Kontoverlauf</h2>

          <div className="ledger-list">
            {dashboard.ledger_entries.map((entry) => (
              <div className="ledger-row" key={entry.id}>
                <div>
                  <strong>{entry.entry_type}</strong>
                  <p>{entry.description}</p>
                </div>
                <span>{formatUsd(entry.amount)}</span>
              </div>
            ))}
          </div>
        </section>
      </section>
    </main>
  )
}

function PlayerGroup({ title, players }: { title: string; players: Player[] }) {
  return (
    <div className="player-group">
      <h3>
        {title} <span>{players.length}</span>
      </h3>

      <div className="player-list">
        {players.map((player) => (
          <article className="player-row" key={player.id}>
            <div>
              <strong>
                {player.first_name} {player.last_name}
              </strong>
              <p>
                {player.position} · {player.nhl_team ?? 'N/A'}
              </p>
            </div>
            <span>{formatUsd(player.market_value)}</span>
          </article>
        ))}
      </div>
    </div>
  )
}

export default App