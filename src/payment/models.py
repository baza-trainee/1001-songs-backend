from sqlalchemy import Column, Integer, String
from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages import FileSystemStorage

from src.database.database import Base

storage = FileSystemStorage(path="static/media/payment_details")


class PaymentDetails(Base):
    __tablename__ = "payment_details"

    id: int = Column(Integer, primary_key=True)
    organization_name: str = Column(String(length=75), nullable=False)
    edrpou: int = Column(Integer, nullable=False)
    bank: str = Column(String(length=50), nullable=False)
    info: str = Column(String(length=100))
    iban: str = Column(String(length=34), nullable=False)
    patreon_url: str = Column(String(length=500), nullable=False)
    coffee_url: str = Column(String(length=500), nullable=False)
    qr_code_url: str = Column(FileType(storage=storage), nullable=False)
