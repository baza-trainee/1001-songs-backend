from typing import Optional
from pydantic import (
    BaseModel,
    Field,
    AnyHttpUrl,
    ValidationInfo,
    field_validator,
    EmailStr,
)

from src.config import settings
from .models import Footer


URL_LEN = Footer.reporting.type.length
EMAIL_LEN = Footer.email.type.length


class FooterSchema(BaseModel):
    reporting: Optional[AnyHttpUrl] = Field(None, max_length=URL_LEN)
    privacy_policy: Optional[AnyHttpUrl] = Field(None, max_length=URL_LEN)
    rules_and_terms: Optional[AnyHttpUrl] = Field(None, max_length=URL_LEN)
    email: Optional[EmailStr] = Field(None, max_length=EMAIL_LEN)
    facebook_url: Optional[AnyHttpUrl] = Field(None, max_length=URL_LEN)
    youtube_url: Optional[AnyHttpUrl] = Field(None, max_length=URL_LEN)

    @field_validator("reporting", "privacy_policy", "rules_and_terms", mode="before")
    @classmethod
    def add_base_url(cls, value: str, info: ValidationInfo) -> str:
        return f"{settings.BASE_URL}/{value}"
