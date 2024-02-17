from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field, ValidationInfo, field_validator

from src.config import settings
from .models import ExpeditionCategory, Expedition


TITLE_CATEGORY_LEN = ExpeditionCategory.title.type.length
CONTENT_LEN = Expedition.content.type.length
AUTHORS_LEN = Expedition.authors.type.item_type.length
EDITORS_LEN = Expedition.editors.type.item_type.length
PHOTOGRAPHERS_LEN = Expedition.photographers.type.item_type.length
RECORDING_LEN = Expedition.recording.type.item_type.length


class ExpeditionCategorySchema(BaseModel):
    id: Optional[int] = Field(..., ge=1)
    title: Optional[str] = Field(..., max_length=TITLE_CATEGORY_LEN)


class ExpedListSchema(BaseModel):
    id: Optional[int] = Field(..., ge=1)
    title: Optional[str]
    location: Optional[str]
    short_description: Optional[str]
    expedition_date: date
    preview_photo: Optional[str] = Field(None)

    @field_validator("location", "preview_photo", mode="before")
    @classmethod
    def add_base_url(cls, value: dict, info: ValidationInfo) -> str:
        match info.field_name:
            case "location":
                return f"{value.name}, {value.region.name}"
            case "preview_photo":
                if value:
                    return f"{settings.BASE_URL}/{value}"


class ExpeditionSchema(BaseModel):
    id: Optional[int] = Field(..., ge=1)
    title: Optional[str]
    location: Optional[str]
    short_description: Optional[str]
    expedition_date: date
    map_photo: Optional[str] = Field(None)
    category: ExpeditionCategorySchema
    content: Optional[str] = Field(None, max_length=CONTENT_LEN)
    authors: Optional[List[str]] = Field(None, max_length=AUTHORS_LEN)
    editors: Optional[List[str]] = Field(None, max_length=EDITORS_LEN)
    photographers: Optional[List[str]] = Field(None, max_length=PHOTOGRAPHERS_LEN)
    recording: Optional[List[str]] = Field(None, max_length=RECORDING_LEN)

    @field_validator("location", "category", "map_photo", mode="before")
    @classmethod
    def add_base_url(cls, value: dict, info: ValidationInfo) -> str:
        match info.field_name:
            case "location":
                return f"{value.name}, {value.region.name}"
            case "map_photo":
                if value:
                    return f"{settings.BASE_URL}/{value}"
            case "category":
                return {"id": value.id, "title": value.title}
