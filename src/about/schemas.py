from pydantic import (
    Field,
    BaseModel,
)

from .models import About

TITLE_LEN = About.title.type.length
CONTENT_LEN = About.content.type.length


class AboutSchema(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(max_length=TITLE_LEN)
    content: str = Field(max_length=CONTENT_LEN)
