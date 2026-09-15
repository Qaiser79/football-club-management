from datetime import datetime, date

from sqlalchemy import DateTime , Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class Coach(Base):
    __tablename__ = "coaches"

    id: Mapped[int] =mapped_column(primary_key=True)

    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"),
        nullable=False
    )

    name: Mapped[str]= mapped_column(
        String(100),
        nullable=False
    )

    role: Mapped[str]=mapped_column(
        String(100),
        nullable=False
    )

    date_of_birth: Mapped[date | None]= mapped_column(
        Date,
        nullable=True
    )

    nationality: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    email: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    bio: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    joined_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="Active",
        nullable=False
    )

    profile_image: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    team: Mapped["Team"] = relationship(
        back_populates="coaches"
    )
