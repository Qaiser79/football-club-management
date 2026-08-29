from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class MatchSquad(Base):
    __tablename__="match_squads"

    __table_args__ = (
        UniqueConstraint(
            "match_id",
            "player_id",
            name = "uq_match_squad_match_player",
        ),
    )

    id: Mapped[int]=mapped_column(primary_key=True)

    match_id: Mapped[int] = mapped_column(
        ForeignKey("matches.id"),
        nullable=False,
    )

    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )