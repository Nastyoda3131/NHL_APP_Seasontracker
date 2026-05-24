export type Player = {
  id: string
  first_name: string
  last_name: string
  position: 'G' | 'D' | 'F'
  nhl_team: string | null
  market_value: string
}

export type LedgerEntry = {
  id: string
  amount: string
  entry_type: string
  description: string
}

export type TeamDashboard = {
  team_id: string
  team_name: string
  owner_name: string
  cash_balance: string
  players: Player[]
  ledger_entries: LedgerEntry[]
}

export async function getTeamDashboard(): Promise<TeamDashboard> {
  const response = await fetch('/api/team/demo')

  if (!response.ok) {
    throw new Error(`Team dashboard request failed: ${response.status}`)
  }

  return response.json()
}