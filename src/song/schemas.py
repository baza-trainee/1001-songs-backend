from typing import Optional

from pydantic import BaseModel, Field, PastDate

from .models import Song


TITLE_LEN = Song.title.type.length
PERFORMERS_LEN = Song.performers.type.length
COLLECTORS_LEN = Song.collectors.type.length
SOURCE_LEN = Song.source.type.length
ARCHIVE_LEN = Song.archive.type.length
REFERENCE_LEN = Song.bibliographic_reference.type.length
COMMENT_LEN = Song.researcher_comment.type.length


class Genre(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., max_length=TITLE_LEN)


class SongSchema(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., max_length=TITLE_LEN)
    recording_date: PastDate
    performers: Optional[str] = Field(None, max_length=PERFORMERS_LEN)
    collectors: Optional[str] = Field(None, max_length=COLLECTORS_LEN)
    source: Optional[str] = Field(None, max_length=SOURCE_LEN)
    archive: Optional[str] = Field(None, max_length=ARCHIVE_LEN)
    bibliographic_reference: Optional[str] = Field(None, max_length=REFERENCE_LEN)
    researcher_comment: Optional[str] = Field(None, max_length=COMMENT_LEN)
    genres: Genre
