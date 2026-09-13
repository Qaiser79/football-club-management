from datetime import datetime, date

from sqlalchemy import DateTime, ForeignKey, String, Integer, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class Player(Base):
    __tablename__="players"
    id: Mapped[int]=mapped_column(primary_key=True)
    team_id: Mapped[int]=mapped_column(ForeignKey("teams.id"))
    name: Mapped[str]=mapped_column(String(100))
    position: Mapped[str]=mapped_column(String(100))
    status: Mapped[str] = mapped_column(
        String(20),
        default="Active",
        nullable=False
    )
    preferred_foot: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    shirt_number: Mapped[int | None]= mapped_column(
        Integer,
        nullable=True
    )

    date_of_birth: Mapped[date | None] = mapped_column(
        Date,
        nullable= True
    )

    nationality: Mapped[str | None] = mapped_column(
        String(100),
        nullable = True
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable= True
    )

    email: Mapped[str | None]= mapped_column(
        String(150),
        nullable=True
    )

    bio: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    height: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    weight: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    joined_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    profile_image: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
    team: Mapped["Team"]=relationship(
        back_populates="players"
    )