from sqlalchemy import Column, Integer, String

from src.database.database import Base


class PaymentDetails(Base):
    __tablename__ = "payment_details"

    id: int = Column(Integer, primary_key=True)
    info: str = Column(String(length=250))
    iban: str = Column(String(length=250))
    coffee_url: str = Column(String(length=500))
    patreon_url: str = Column(String(length=500))
    qr_code_url: str = Column(String(length=500))
