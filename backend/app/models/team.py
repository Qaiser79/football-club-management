from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class Team(Base):
    __tablename__="teams"
    id: Mapped[int]=mapped_column(primary_key=True)
    club_id: Mapped[int]=mapped_column(
        ForeignKey("clubs.id"),
        nullable=False
    )

    name: Mapped[str]=mapped_column(
        String(100),
        nullable=False  
        )
    
    team_type: Mapped[str]=mapped_column(
        String(50),
        nullable=False,
    )

    created_at: Mapped[datetime]= mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
   )
    
    club: Mapped["Club"]=relationship(
        back_populates="teams"
    )
    players: Mapped[list["Player"]]=relationship(
        back_populates="team"
    )

    matches: Mapped[list["Match"]] = relationship(
        back_populates="team"
    )