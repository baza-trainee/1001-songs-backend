from datetime import date
from typing import List, Optional

from pydantic import AnyHttpUrl, BaseModel, Field, ValidationInfo, field_validator

from src.config import settings
from .models import OurProject


TITLE_LEN = OurProject.title.type.length
CONTENT_LEN = OurProject.content.type.length
DESCRIPTION_LEN = OurProject.short_description.type.length
AUTHORS_LEN = OurProject.authors.type.item_type.length
EDITORS_LEN = OurProject.editors.type.item_type.length
PHOTOGRAPHERS_LEN = OurProject.photographers.type.item_type.length
RECORDING_LEN = OurProject.recording.type.item_type.length
RECORDING_LEN = OurProject.recording.type.item_type.length


class ProjectSliderSchema(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., max_length=TITLE_LEN)
    short_description: Optional[str] = Field(None, max_length=DESCRIPTION_LEN)
    preview_photo: AnyHttpUrl

    @field_validator("preview_photo", mode="before")
    @classmethod
    def add_base_url(cls, value: dict, info: ValidationInfo) -> str:
        match info.field_name:
            case "preview_photo":
                if value and not value.startswith(("https://", "http://")):
                    return f"{settings.BASE_URL}/{value}"
                return value


class ProjectSchema(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., max_length=TITLE_LEN)
    location: Optional[str]
    project_date: date
    content: Optional[str] = Field(None, max_length=CONTENT_LEN)
    authors: Optional[List[str]] = Field(None, max_length=AUTHORS_LEN)
    editors: Optional[List[str]] = Field(None, max_length=EDITORS_LEN)
    photographers: Optional[List[str]] = Field(None, max_length=PHOTOGRAPHERS_LEN)
    recording: Optional[List[str]] = Field(None, max_length=RECORDING_LEN)

    @field_validator("location", mode="before")
    @classmethod
    def add_base_url(cls, value: dict, info: ValidationInfo) -> str:
        match info.field_name:
            case "location":
                if isinstance(value, dict):
                    return f'{value.get("name")}, {value.get("region").get("name")}, {value.get("country").get("name")}'
                return f"{value.name}, {value.region.name}, {value.country.name}"
