import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def uuid_str() -> str:
    return str(uuid.uuid4())


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    login_code: Mapped[str] = mapped_column(String(120), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)

    team: Mapped["FantasyTeam"] = relationship(back_populates="user", uselist=False)


class FantasyTeam(Base):
    __tablename__ = "fantasy_teams"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    cash_balance: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)

    user: Mapped[User] = relationship(back_populates="team")
    players: Mapped[list["TeamPlayer"]] = relationship(back_populates="team")
    ledger_entries: Mapped[list["LedgerEntry"]] = relationship(back_populates="team")


class NhlPlayer(Base):
    __tablename__ = "nhl_players"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    nhl_player_id: Mapped[str | None] = mapped_column(String(50), unique=True, nullable=True)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    position: Mapped[str] = mapped_column(String(20), nullable=False)  # G, D, F
    nhl_team: Mapped[str | None] = mapped_column(String(10), nullable=True)
    market_value: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=60000)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)

    ownerships: Mapped[list["TeamPlayer"]] = relationship(back_populates="player")


class TeamPlayer(Base):
    __tablename__ = "team_players"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    team_id: Mapped[str] = mapped_column(String(36), ForeignKey("fantasy_teams.id"), nullable=False)
    player_id: Mapped[str] = mapped_column(String(36), ForeignKey("nhl_players.id"), nullable=False)
    acquired_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    released_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    team: Mapped[FantasyTeam] = relationship(back_populates="players")
    player: Mapped[NhlPlayer] = relationship(back_populates="ownerships")

    __table_args__ = (
        UniqueConstraint("player_id", "released_at", name="uq_active_player_ownership"),
    )


class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    team_id: Mapped[str] = mapped_column(String(36), ForeignKey("fantasy_teams.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    entry_type: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)

    team: Mapped[FantasyTeam] = relationship(back_populates="ledger_entries")


class AppConfig(Base):
    __tablename__ = "app_config"

    key: Mapped[str] = mapped_column(String(120), primary_key=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)