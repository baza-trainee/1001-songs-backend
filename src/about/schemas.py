from pydantic import (
    Field,
    BaseModel,
)

from .models import About

CONTENT_LEN = About.content.type.length


class AboutSchema(BaseModel):
    id: int = Field(..., ge=1)
    content: str = Field(max_length=CONTENT_LEN)
