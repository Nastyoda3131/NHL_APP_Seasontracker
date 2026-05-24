from decimal import Decimal

from pydantic import BaseModel


class UserRead(BaseModel):
    id: str
    display_name: str
    is_admin: bool

    model_config = {"from_attributes": True}


class PlayerRead(BaseModel):
    id: str
    first_name: str
    last_name: str
    position: str
    nhl_team: str | None
    market_value: Decimal

    model_config = {"from_attributes": True}


class LedgerEntryRead(BaseModel):
    id: str
    amount: Decimal
    entry_type: str
    description: str

    model_config = {"from_attributes": True}


class TeamDashboardRead(BaseModel):
    team_id: str
    team_name: str
    owner_name: str
    cash_balance: Decimal
    players: list[PlayerRead]
    ledger_entries: list[LedgerEntryRead]