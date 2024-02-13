from pydantic import AnyHttpUrl, Field, BaseModel, ValidationInfo, field_validator

from src.config import settings
from .models import PaymentDetails

ORGANIZATION_NAME = PaymentDetails.organization_name.type.length
EDRPOU_LEN = PaymentDetails.edrpou.type.length
BANK_LEN = PaymentDetails.bank.type.length
INFO_LEN = PaymentDetails.info.type.length
IBAN_LEN = PaymentDetails.iban.type.length
COFFEE_URL_LEN = PaymentDetails.coffee_url.type.length
PATREON_URL_LEN = PaymentDetails.patreon_url.type.length
QR_CODE_URL_LEN = PaymentDetails.qr_code_url.type.length


class PaymentDetailsSchema(BaseModel):
    id: int
    organization_name: str = Field(max_length=ORGANIZATION_NAME)
    edrpou: str = Field(max_length=EDRPOU_LEN)
    bank: str = Field(max_length=BANK_LEN)
    info: str = Field(max_length=INFO_LEN)
    iban: str = Field(max_length=IBAN_LEN)
    coffee_url: AnyHttpUrl = Field(max_length=COFFEE_URL_LEN)
    patreon_url: AnyHttpUrl = Field(max_length=PATREON_URL_LEN)
    qr_code_url: AnyHttpUrl = Field(max_length=QR_CODE_URL_LEN)

    @field_validator("qr_code_url", mode="before")
    @classmethod
    def add_base_url(cls, value: str, info: ValidationInfo) -> str:
        return f"{settings.BASE_URL}/{value}"
