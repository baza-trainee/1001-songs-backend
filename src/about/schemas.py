from pydantic import (
    Field,
    BaseModel,
)

from .models import About

CONTENT_LEN = About.content.type.length
SLIDER_CAPTION_LEN = About.slider_caption.type.length


class AboutSchema(BaseModel):
    id: int = Field(..., ge=1)
    content: str = Field(max_length=CONTENT_LEN)
    slider_caption: str = Field(max_length=SLIDER_CAPTION_LEN)
