from datetime import datetime
from typing import Annotated, Optional, List

from pydantic import AnyHttpUrl, BaseModel, Field, ValidationInfo, field_validator

from src.config import settings

from .models import NewsCategory, News


NAME_LEN = NewsCategory.name.type.length
TITLE_LEN = News.title.type.length
CONTENT_LEN = News.content.type.length
SLIDER_CAPTION_LEN = News.slider_caption.type.length
AUTHORS_LEN = News.authors.type.item_type.length
EDITORS_LEN = News.editors.type.item_type.length
PHOTOGRAPHERS_LEN = News.photographers.type.item_type.length
PREVIEW_PHOTO_LEN = News.preview_photo.type.length
LOCATION_LEN = News.preview_photo.type.length


class NewCategorySchema(BaseModel):
    id: int = Field(..., ge=1)
    name: str = Field(..., max_length=NAME_LEN)


class NewsSchema(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., max_length=TITLE_LEN)
    content: str = Field(..., max_length=CONTENT_LEN)
    slider_caption: Optional[str] = Field(None, max_length=SLIDER_CAPTION_LEN)
    authors: Optional[List[Annotated[str, Field(max_length=AUTHORS_LEN)]]] = Field([])
    editors: Optional[List[Annotated[str, Field(max_length=EDITORS_LEN)]]] = Field([])
    photographers: Optional[
        List[Annotated[str, Field(max_length=PHOTOGRAPHERS_LEN)]]
    ] = Field([])
    preview_photo: AnyHttpUrl
    location: Optional[str] = Field(None)
    category: NewCategorySchema
    created_at: datetime

    @field_validator("location", "preview_photo", mode="before")
    @classmethod
    def add_base_url(cls, value: dict, info: ValidationInfo) -> str:
        match info.field_name:
            case "location":
                return f"{value.name}, {value.region.name}, {value.region.country.name}"
            case "preview_photo":
                if value:
                    return f"{settings.BASE_URL}/{value}"
