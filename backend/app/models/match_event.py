from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class MatchEvent(Base):
    __tablename__ = "match_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    match_id: Mapped[int] = mapped_column(
        ForeignKey("matches.id"),
        nullable=False
    )

    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id"),
        nullable=False
    )

    related_player_id: Mapped[int | None] = mapped_column(
        ForeignKey("players.id"),
        nullable=True
    )

    event_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    minute: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    match: Mapped["Match"] = relationship()

    player: Mapped["Player"] = relationship(
        foreign_keys=[player_id]
    )

    related_player: Mapped["Player"] = relationship(
        foreign_keys=[related_player_id]
    )