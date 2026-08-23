from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int]= mapped_column(primary_key=True)

    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"),
        nullable=False
    )

    opponent_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    match_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable= False
    )

    competition: Mapped[str | None]= mapped_column(
        String(100),
        nullable=False
    )
    venue: Mapped[str | None]= mapped_column(
        String(100),
        nullable=True
    )

    is_home: Mapped[bool] = mapped_column(
        Boolean,
        nullable= False
    )

    our_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    opponent_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="scheduled",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    team: Mapped["Team"] = relationship(
        back_populates="matches"
    )