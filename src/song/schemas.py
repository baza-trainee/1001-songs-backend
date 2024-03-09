from pydantic import BaseModel, Field

from .models import Song


TITLE_LEN = Song.title.type.length


class Genre(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., max_length=TITLE_LEN)
