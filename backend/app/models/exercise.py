from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    objective: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    difficulty: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    players_required: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    default_duration_minutes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    equipment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    coaching_points: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )