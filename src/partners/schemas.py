from typing import Optional

from pydantic import BaseModel, Field, AnyHttpUrl, ValidationInfo, field_validator

from src.config import settings
from .models import Partners


LINK_LEN = Partners.link.type.length
PHOTO_LEN = Partners.photo.type.length


class PartnersSchema(BaseModel):
    id: Optional[int] = Field(..., ge=1)
    link: Optional[str] = Field(None, max_length=LINK_LEN)
    photo: AnyHttpUrl = Field(..., max_length=PHOTO_LEN)

    @field_validator("photo", mode="before")
    @classmethod
    def add_base_url(cls, value: str, info: ValidationInfo) -> str:
        return f"{settings.BASE_URL}/{value}"
