from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FantasyTeam, LedgerEntry, NhlPlayer, TeamPlayer, User


router = APIRouter(prefix="/api/dev", tags=["dev"])


@router.post("/seed")
def seed_demo_data(db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.display_name == "Dominik").first()
    if existing_user:
        return {"status": "already_seeded"}

    user = User(
        display_name="Dominik",
        login_code="1234",
        is_admin=True,
    )
    db.add(user)
    db.flush()

    team = FantasyTeam(
        user_id=user.id,
        name="Dominik HC",
        cash_balance=Decimal("1000000.00"),
    )
    db.add(team)
    db.flush()

    players = [
        NhlPlayer(first_name="Connor", last_name="McDavid", position="F", nhl_team="EDM", market_value=Decimal("1000000.00")),
        NhlPlayer(first_name="Auston", last_name="Matthews", position="F", nhl_team="TOR", market_value=Decimal("950000.00")),
        NhlPlayer(first_name="Leon", last_name="Draisaitl", position="F", nhl_team="EDM", market_value=Decimal("920000.00")),
        NhlPlayer(first_name="Nathan", last_name="MacKinnon", position="F", nhl_team="COL", market_value=Decimal("930000.00")),
        NhlPlayer(first_name="David", last_name="Pastrnak", position="F", nhl_team="BOS", market_value=Decimal("870000.00")),
        NhlPlayer(first_name="Mikko", last_name="Rantanen", position="F", nhl_team="COL", market_value=Decimal("840000.00")),
        NhlPlayer(first_name="Cale", last_name="Makar", position="D", nhl_team="COL", market_value=Decimal("900000.00")),
        NhlPlayer(first_name="Quinn", last_name="Hughes", position="D", nhl_team="VAN", market_value=Decimal("850000.00")),
        NhlPlayer(first_name="Adam", last_name="Fox", position="D", nhl_team="NYR", market_value=Decimal("780000.00")),
        NhlPlayer(first_name="Roman", last_name="Josi", position="D", nhl_team="NSH", market_value=Decimal("760000.00")),
        NhlPlayer(first_name="Victor", last_name="Hedman", position="D", nhl_team="TBL", market_value=Decimal("720000.00")),
        NhlPlayer(first_name="Rasmus", last_name="Dahlin", position="D", nhl_team="BUF", market_value=Decimal("740000.00")),
        NhlPlayer(first_name="Igor", last_name="Shesterkin", position="G", nhl_team="NYR", market_value=Decimal("800000.00")),
    ]

    db.add_all(players)
    db.flush()

    for player in players:
        db.add(
            TeamPlayer(
                team_id=team.id,
                player_id=player.id,
            )
        )

    db.add(
        LedgerEntry(
            team_id=team.id,
            amount=Decimal("1000000.00"),
            entry_type="start_cash",
            description="Initial start cash",
        )
    )

    db.commit()

    return {
        "status": "seeded",
        "user": user.display_name,
        "team": team.name,
        "players": len(players),
    }