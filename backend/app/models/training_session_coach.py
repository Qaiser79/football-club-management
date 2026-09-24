from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class TrainingSessionCoach(Base):
    __tablename__ = "training_session_coaches"

    id: Mapped[int] = mapped_column(primary_key=True)

    training_session_id: Mapped[int] = mapped_column(
        ForeignKey("training_sessions.id"),
        nullable=False,
    )

    coach_id: Mapped[int] = mapped_column(
        ForeignKey("coaches.id"),
        nullable=False,
    )

    training_session = relationship("TrainingSession")

    coach = relationship("Coach")

    __table_args__ = (
        UniqueConstraint(
            "training_session_id",
            "coach_id",
            name="uq_training_session_coach",
        ),
    )