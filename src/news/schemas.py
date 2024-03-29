from datetime import date
from typing import Annotated, Optional, List

from pydantic import AnyHttpUrl, BaseModel, Field, ValidationInfo, field_validator

from src.config import settings
from .models import NewsCategory, News


NAME_LEN = NewsCategory.name.type.length
TITLE_LEN = News.title.type.length
SHORT_DESCRIPTION_LEN = News.short_description.type.length
CONTENT_LEN = News.content.type.length
AUTHORS_LEN = News.authors.type.item_type.length
EDITORS_LEN = News.editors.type.item_type.length
PHOTOGRAPHERS_LEN = News.photographers.type.item_type.length
PREVIEW_PHOTO_LEN = News.preview_photo.type.length
LOCATION_LEN = News.preview_photo.type.length


class NewCategorySchema(BaseModel):
    id: int = Field(ge=1)
    name: str = Field(max_length=NAME_LEN)


class NewsSchemaList(BaseModel):
    id: int = Field(ge=1)
    title: str = Field(max_length=TITLE_LEN)
    short_description: str = Field(max_length=SHORT_DESCRIPTION_LEN)
    preview_photo: AnyHttpUrl
    created_at: date
    category: NewCategorySchema
    location: str

    @field_validator("location", "preview_photo", mode="before")
    @classmethod
    def add_base_url(cls, value: dict, info: ValidationInfo) -> str:
        match info.field_name:
            case "location":
                if isinstance(value, str):
                    return value
                elif isinstance(value, dict):
                    return f'{value.get("name")}, {value.get("region").get("name")}, {value.get("country").get("name")}'
                return f"{value.name}, {value.region.name}, {value.country.name}"
            case "preview_photo":
                if value and not value.startswith(("https://", "http://")):
                    return f"{settings.BASE_URL}/{value}"
                return value


class NewsSchema(NewsSchemaList):
    content: str = Field(..., max_length=CONTENT_LEN)
    authors: Optional[List[Annotated[str, Field(max_length=AUTHORS_LEN)]]] = Field([])
    editors: Optional[List[Annotated[str, Field(max_length=EDITORS_LEN)]]] = Field([])
    photographers: Optional[
        List[Annotated[str, Field(max_length=PHOTOGRAPHERS_LEN)]]
    ] = Field([])
