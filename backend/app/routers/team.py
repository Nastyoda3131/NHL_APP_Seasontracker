from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import FantasyTeam, TeamPlayer
from app.schemas import LedgerEntryRead, PlayerRead, TeamDashboardRead


router = APIRouter(prefix="/api/team", tags=["team"])


@router.get("/demo", response_model=TeamDashboardRead)
def get_demo_team(db: Session = Depends(get_db)):
    team = (
        db.query(FantasyTeam)
        .options(
            joinedload(FantasyTeam.user),
            joinedload(FantasyTeam.players).joinedload(TeamPlayer.player),
            joinedload(FantasyTeam.ledger_entries),
        )
        .first()
    )

    if team is None:
        raise HTTPException(
            status_code=404,
            detail="No team found. Run POST /api/dev/seed first.",
        )

    active_players = [
        team_player.player
        for team_player in team.players
        if team_player.released_at is None
    ]

    return TeamDashboardRead(
        team_id=team.id,
        team_name=team.name,
        owner_name=team.user.display_name,
        cash_balance=team.cash_balance,
        players=[PlayerRead.model_validate(player) for player in active_players],
        ledger_entries=[
            LedgerEntryRead.model_validate(entry)
            for entry in sorted(team.ledger_entries, key=lambda item: item.created_at)
        ],
    )