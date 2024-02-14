from datetime import datetime
from typing import Annotated, Optional, List

from pydantic import BaseModel, Field

from .models import NewsCategory, News


NAME_LEN = NewsCategory.name.type.length
TITLE_LEN = News.title.type.length
CONTENT_LEN = News.content.type.length
SLIDER_CAPTION_LEN = News.slider_caption.type.length
AUTHORS_LEN = News.authors.type.item_type.length
EDITORS_LEN = News.editors.type.item_type.length
PHOTOGRAPHERS_LEN = News.photographers.type.item_type.length


class NewCategorySchema(BaseModel):
    id: int = Field(..., ge=1)
    name: str = Field(..., max_length=NAME_LEN)


class NewsSchema(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., max_length=TITLE_LEN)
    content: str = Field(..., max_length=CONTENT_LEN)
    slider_caption: Optional[str] = Field(None, max_length=SLIDER_CAPTION_LEN)
    authors: Optional[List[str]] = Field(None, max_length=AUTHORS_LEN)
    editors: Optional[List[str]] = Field(None, max_length=EDITORS_LEN)
    photographers: Optional[List[str]] = Field(None, max_length=PHOTOGRAPHERS_LEN)
    category: NewCategorySchema
    created_at: datetime
