from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class Club(Base):
    __tablename__="clubs"
    id: Mapped[int]=mapped_column(primary_key=True)
    organization_id: Mapped[int]=mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
    )

    name: Mapped[str | None]=mapped_column(
        String(100),
        nullable=False,
    )

    short_name: Mapped[str | None]= mapped_column(
        String(20),
        nullable=True,
    )

    country: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    created_at: Mapped[datetime]=mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    organization: Mapped["Organization"]=relationship(
        back_populates="clubs"
    )
    teams: Mapped[list["Team"]]=relationship(
        back_populates="club"
    )