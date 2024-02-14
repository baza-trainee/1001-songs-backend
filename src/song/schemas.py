from pydantic import BaseModel, Field

from .models import Song


TITLE_LEN = Song.title.type.length
PERFORMERS_LEN = Song.performers.type.length
COLLECTORS_LEN = Song.collectors.type.length
SOURCE_LEN = Song.source.type.length
ARCHIVE_LEN = Song.archive.type.length


class Genre(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., max_length=TITLE_LEN)
