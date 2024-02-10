from typing import List, Optional

from pydantic import BaseModel, Field, AnyHttpUrl, ValidationInfo, field_validator

from src.config import settings
from .models import EducationSection


TITLE_LEN = EducationSection.title.type.length
DESCRIPTION_LEN = EducationSection.description.type.length
MEDIA_LEN = EducationSection.media1.type.length


class EducationSchema(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., max_length=TITLE_LEN)
    media: Optional[List[AnyHttpUrl]] = Field(None, max_items=5)
    description: Optional[str] = Field(None, max_length=DESCRIPTION_LEN)

    @field_validator("media", mode="before")
    @classmethod
    def add_base_url(cls, value: List[str], info: ValidationInfo) -> str:
        result = []
        for url in value:
            if url:
                result.append(f"{settings.BASE_URL}/{url}")
        return result
