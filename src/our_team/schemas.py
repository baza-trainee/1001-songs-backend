from typing import Optional

from pydantic import BaseModel, Field, AnyHttpUrl, ValidationInfo, field_validator

from src.config import settings
from .models import OurTeam


FULL_NAME_LEN = OurTeam.full_name.type.length
PHOTO_LEN = OurTeam.photo.type.length
DESCRIPTION_LEN = OurTeam.description.type.length


class OurTeamSchema(BaseModel):
    id: Optional[int] = Field(..., ge=1)
    full_name: Optional[str] = Field(..., max_length=FULL_NAME_LEN)
    photo: AnyHttpUrl = Field(None, max_length=PHOTO_LEN)
    description: Optional[str] = Field(..., max_length=DESCRIPTION_LEN)

    @field_validator("photo", mode="before")
    @classmethod
    def add_base_url(cls, value: str, info: ValidationInfo) -> str:
        return f"{settings.BASE_URL}/{value}"
