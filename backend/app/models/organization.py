from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column,relationship

from app.database import Base

class Organization(Base):
    __tablename__="organizations"

    id: Mapped[int]= mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(100), nullable=False, unique=True)
    created_at: Mapped[datetime]=mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    clubs: Mapped[list["Club"]]=relationship(
        back_populates="organization"
    )
