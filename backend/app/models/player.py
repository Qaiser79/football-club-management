from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
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
        default="Active"
    )
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
    team: Mapped["Team"]=relationship(
        back_populates="players"
    )