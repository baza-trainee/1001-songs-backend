from typing import List, Optional

from pydantic import BaseModel, Field, AnyHttpUrl, ValidationInfo, field_validator

from src.config import settings
from .models import EducationPage, EducationPageSongGenre, CalendarAndRitualCategory


TITLE_LEN = EducationPage.title.type.length
DESCRIPTION_LEN = EducationPage.description.type.length
EDUCATION_GENRE_DESCRIPTION_LEN = EducationPageSongGenre.description.type.length
CALENDAR_AND_RITUAL_CATEGORY_LEN = CalendarAndRitualCategory.description.type.length
RECOMENDATIONS_LEN = EducationPage.recommendations.type.length
SOURCES_LEN = EducationPage.recommended_sources.type.length


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

    class Config:
        from_attributes = True


class SubCategoryBaseSchema(BaseCycleSchema):
    education_genres: List[EducationGenreBaseSchema]

    @field_validator("education_genres", mode="before")
    @classmethod
    def sort_education_genres(cls, value: List[str], info: ValidationInfo) -> str:
        return sorted(value, key=lambda x: x.get("id") if isinstance(x, dict) else x.id)


class EducationGenreSchema(EducationGenreBaseSchema):
    media: List[AnyHttpUrl] = Field(max_length=5)
    description: Optional[str] = Field(None, max_length=EDUCATION_GENRE_DESCRIPTION_LEN)
    main_category: EducationGenreBaseSchema

    @field_validator("media", mode="before")
    @classmethod
    def add_base_url(cls, value: List[str], info: ValidationInfo) -> str:
        result = []
        for url in value:
            if url:
                if not url.startswith(("https://", "http://")):
                    result.append(f"{settings.BASE_URL}/{url}")
                else:
                    result.append(url)
        return result

    class Config:
        from_attributes = True


class EducationSchema(BaseModel):
    title: str = Field(..., max_length=TITLE_LEN)
    description: Optional[str] = Field(None, max_length=DESCRIPTION_LEN)
    recommendations: Optional[str] = Field(None, max_length=RECOMENDATIONS_LEN)
    recommended_sources: Optional[str] = Field(None, max_length=SOURCES_LEN)
    calendar_and_ritual_categories: List[BaseCycleSchema]


class CategorySchema(EducationGenreBaseSchema):
    description: Optional[str] = Field(
        None, max_length=CALENDAR_AND_RITUAL_CATEGORY_LEN
    )
    recommended_sources: Optional[str] = Field(None, max_length=SOURCES_LEN)
    song_subcategories: List[SubCategoryBaseSchema]

    @field_validator("song_subcategories", mode="before")
    @classmethod
    def sort_subcategories(cls, value: List[str], info: ValidationInfo) -> str:
        return sorted(value, key=lambda x: x.get("id") if isinstance(x, dict) else x.id)


class GenreSchema(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., max_length=TITLE_LEN)


class SongsSchema(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., max_length=TITLE_LEN)
    stereo_audio: Optional[AnyHttpUrl] = Field(None)
    photos: Optional[List[AnyHttpUrl]] = Field([], max_length=5)
    recording_location: Optional[str] = Field(None, max_length=100)
    genres: str

    @field_validator("photos", "stereo_audio", mode="before")
    @classmethod
    def add_base_url(cls, value: List[str], info: ValidationInfo) -> str:
        match info.field_name:
            case "photos":
                result = []
                for url in value:
                    if url and not url.startswith(("https://", "http://")):
                        result.append(f"{settings.BASE_URL}/{url}")
                    else:
                        result.append(url)
                return result
            case "stereo_audio":
                if value and not value.startswith(("https://", "http://")):
                    return f"{settings.BASE_URL}/{value}"
                else:
                    return value
            case _:
                if value:
                    return f"{settings.BASE_URL}/{value}"


class SubCategorySchema(BaseModel):
    id: int
    title: str


class GenreForSongPageSchema(BaseModel):
    id: int
    title: str
    sub_category: SubCategorySchema
    main_category: EducationGenreBaseSchema


class OneSongSchema(BaseModel):
    id: int = Field(..., ge=1)
    genres: List[GenreForSongPageSchema] = Field(
        ..., validation_alias="education_genres"
    )
    title: str = Field(..., max_length=TITLE_LEN)
    stereo_audio: Optional[AnyHttpUrl] = Field(None)
    song_text: Optional[str] = Field(None)
    song_description: Optional[str] = Field(None)
    location: str = Field(..., validation_alias="city")
    ethnographic_district: str
    collectors: Optional[List[str]] = Field(None)
    performers: str
    video_url: Optional[AnyHttpUrl] = Field(None)
    comment_map: Optional[str] = Field(None)
    map_photo: Optional[AnyHttpUrl] = Field(None)
    photos: Optional[List[AnyHttpUrl]] = Field(
        None, max_length=5, validation_alias="ethnographic_photos"
    )

    @field_validator(
        "photos", "stereo_audio", "map_photo", "location", "genres", mode="before"
    )
    @classmethod
    def modify_fields(cls, value: str, info: ValidationInfo) -> str:
        match info.field_name:
            case "photos":
                result = []
                for url in value:
                    if url:
                        result.append(f"{settings.BASE_URL}/{url}")
                return result
            case "stereo_audio" | "map_photo":
                if value:
                    return f"{settings.BASE_URL}/{value}"
            case "genres":
                if value:
                    return [
                        {
                            "id": genre.id,
                            "title": genre.title,
                            "sub_category": {
                                "id": genre.sub_category.id,
                                "title": genre.sub_category.title,
                            },
                            "main_category": {
                                "id": genre.main_category.id,
                                "title": genre.main_category.title,
                            },
                        }
                        for genre in value
                    ]
                return []
            case "location":
                return f"{value.name}, {value.region.name}, {value.country.name}"
