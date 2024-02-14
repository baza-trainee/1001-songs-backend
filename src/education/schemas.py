from typing import List, Optional

from pydantic import BaseModel, Field, AnyHttpUrl, ValidationInfo, field_validator

from src.config import settings
from .models import EducationPage


TITLE_LEN = EducationPage.title.type.length
DESCRIPTION_LEN = EducationPage.description.type.length
RECOMENDATIONS_LEN = EducationPage.recommendations.type.length
SOURCES_LEN = EducationPage.recommended_sources.type.item_type.length


class BaseCycleSchema(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., max_length=TITLE_LEN)
    media: Optional[AnyHttpUrl] = Field(None)

    @field_validator("media", mode="before")
    @classmethod
    def add_base_url(cls, value: str, info: ValidationInfo) -> str:
        if value:
            return f"{settings.BASE_URL}/{value}"


class EducationGenreBaseSchema(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., max_length=TITLE_LEN)


class SubCategoryBaseSchema(BaseCycleSchema):
    education_genres: List[EducationGenreBaseSchema]


class EducationGenreSchema(EducationGenreBaseSchema):
    media: Optional[List[AnyHttpUrl]] = Field(None, max_items=5)
    description: Optional[str] = Field(None, max_length=DESCRIPTION_LEN)

    @field_validator("media", mode="before")
    @classmethod
    def add_base_url(cls, value: List[str], info: ValidationInfo) -> str:
        result = []
        for url in value:
            if url:
                result.append(f"{settings.BASE_URL}/{url}")
        return result


class EducationSchema(BaseModel):
    title: str = Field(..., max_length=TITLE_LEN)
    description: Optional[str] = Field(None, max_length=DESCRIPTION_LEN)
    recommendations: Optional[str] = Field(None, max_length=RECOMENDATIONS_LEN)
    recommended_sources: Optional[str] = Field(None, max_length=SOURCES_LEN)
    calendar_and_ritual_categories: List[BaseCycleSchema]


class CategorySchema(EducationGenreBaseSchema):
    description: Optional[str] = Field(None, max_length=DESCRIPTION_LEN)
    recommendations: Optional[str] = Field(None, max_length=RECOMENDATIONS_LEN)
    song_subcategories: List[SubCategoryBaseSchema]


class GenreSchema(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., max_length=TITLE_LEN)


class SongsSchema(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., max_length=TITLE_LEN)
    stereo_audio: Optional[AnyHttpUrl] = Field(None)
    photos: Optional[List[AnyHttpUrl]] = Field(None, max_items=5)
    recording_location: Optional[str] = Field(None, max_length=100)
    genre: str

    @field_validator("photos", "stereo_audio", mode="before")
    @classmethod
    def add_base_url(cls, value: List[str], info: ValidationInfo) -> str:
        if value == "photos":
            result = []
            for url in value:
                if url:
                    result.append(f"{settings.BASE_URL}/{url}")
            return result
        else:
            if value:
                return f"{settings.BASE_URL}/{value}"


class OneSongSchema(BaseModel):
    id: int = Field(..., ge=1)
    genres: Optional[List[str]]
    title: str = Field(..., max_length=TITLE_LEN)
    stereo_audio: Optional[AnyHttpUrl] = Field(None)
    song_text: Optional[str]
    song_description: Optional[str]
    location: str
    ethnographic_district: str
    collectors: str
    performers: str
    video_url: Optional[str]
    comment_map: Optional[str]
    map_photo: Optional[AnyHttpUrl]
    photos: Optional[List[AnyHttpUrl]] = Field(None, max_items=5)

    @field_validator("photos", "stereo_audio", "map_photo", mode="before")
    @classmethod
    def add_base_url(cls, value: List[str], info: ValidationInfo) -> str:
        if isinstance(value, list):
            result = []
            for url in value:
                if url:
                    result.append(f"{settings.BASE_URL}/{url}")
            return result
        else:
            if value:
                return f"{settings.BASE_URL}/{value}"
            else:
                return None
