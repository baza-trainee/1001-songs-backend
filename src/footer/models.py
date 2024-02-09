from sqlalchemy import Column, String, Integer

from src.database.database import Base


class Footer(Base):
    __tablename__ = "footer"

    id: int = Column(Integer, primary_key=True)
    reporting: str = Column(String(500))
    privacy_policy: str = Column(String(500))
    rules_and_terms: str = Column(String(500))
    email: str = Column(String(length=100))
    facebook_url: str = Column(String(length=500))
    youtube_url: str = Column(String(length=500))
