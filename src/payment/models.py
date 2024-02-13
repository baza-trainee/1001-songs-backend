from sqlalchemy import Column, Integer, String
from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages import FileSystemStorage

from src.database.database import Base

storage = FileSystemStorage(path="static/media/payment_details")


class PaymentDetails(Base):
    __tablename__ = "payment_details"

    id: int = Column(Integer, primary_key=True)
    organization_name: str = Column(String(length=250))
    edrpou: str = Column(String(length=250))
    bank: str = Column(String(length=250))
    info: str = Column(String(length=250))
    iban: str = Column(String(length=250))
    coffee_url: str = Column(String(length=500))
    patreon_url: str = Column(String(length=500))
    qr_code_url: str = Column(FileType(storage=storage))
