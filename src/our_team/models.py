from sqlalchemy import Column, String, Integer

from src.database.database import Base


class OurTeam(Base):
    __tablename__ = "our_team"

    id: int = Column(Integer, primary_key=True)
    full_name: str = Column(String(100), nullable=False)
    photo: str = Column(String(500))
    description: str = Column(String(500))
