from typing import List, Optional
from datetime import date

from pydantic import (
    AnyHttpUrl,
    BaseModel,
    Field,
    ValidationInfo,
    field_validator,
)

from src.config import settings
from src.song.models import Fund, Genre
from .models import City


NAME_LEN = City.name.type.length
NAME_GENRE_LEN = Genre.genre_name.type.length
FUND_LEN = Fund.title.type.length


class FundSchema(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., max_length=NAME_LEN)


class BaseLocation(BaseModel):
    id: int = Field(..., ge=1)
    name: str = Field(..., max_length=NAME_LEN)


class CountrySchema(BaseLocation):
    song_count: int = Field(..., ge=1)


class RegionSchema(BaseLocation):
    song_count: int = Field(..., ge=1)
    country_id: int = Field(..., ge=1)


class CitySchema(BaseLocation):
    country_id: int = Field(..., ge=1)
    region_id: int = Field(..., ge=1)
    song_count: int = Field(..., ge=1)


class GenreFilterSchema(BaseModel):
    id: int = Field(..., ge=1)
    name: str = Field(..., max_length=NAME_GENRE_LEN)
    song_count: int = Field(..., ge=1)


class FundFilterSchema(BaseModel):
    id: int = Field(..., ge=1)
    name: str = Field(..., max_length=NAME_GENRE_LEN)
    song_count: int = Field(..., ge=1)


class CityMapSchema(BaseModel):
    latitude: Optional[float] = Field(None, examples=[51.53694777241224])
    longitude: Optional[float] = Field(None, examples=[26.98664264])


class FilterMapSchema(BaseModel):
    id: int = Field(..., ge=1)
    city: str
    latitude: float = Field(..., examples=[51.53694777241224])
    longitude: Optional[float] = Field(..., examples=[26.98664264])
    song_count: int = Field(..., ge=1)


class FilterSongSchema(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(...)
    song_text: Optional[str] = Field(None)
    collectors: Optional[List[str]] = Field(None)
    recording_date: date
    stereo_audio: Optional[str] = Field(None)
    video_url: Optional[str] = Field(None)
    ethnographic_district: Optional[str]
    photos: Optional[List[AnyHttpUrl]] = Field(None)
    city: str
    genres: List[str]
    education_genres: List[str]
    fund: str

    @field_validator(
        "city",
        "photos",
        "genres",
        "fund",
        "education_genres",
        "stereo_audio",
        mode="before",
    )
    @classmethod
    def modify_fields(cls, value: str, info: ValidationInfo) -> str:
        match info.field_name:
            case "photos":
                result = []
                for url in value:
                    if url and not url.startswith(("https://", "http://")):
                        result.append(f"{settings.BASE_URL}/{url}")
                return result
            case "city":
                if value and not isinstance(value, str):
                    city_name = value.name
                    region_name = value.region.name
                    return f"{city_name}, {region_name}"
                return value
            case "genres":
                return [
                    genre.genre_name if not isinstance(genre, str) else genre
                    for genre in value
                ]
            case "fund":
                if value and not isinstance(value, str):
                    return value.title
                return value
            case "education_genres":
                return [
                    genre.title if not isinstance(genre, str) else genre
                    for genre in value
                ]
            case "stereo_audio":
                if value and not value.startswith(("https://", "http://")):
                    return f"{settings.BASE_URL}/{value}"
                return value


class SongMapPageSchema(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(...)
    song_text: Optional[str] = Field(None)
    genres: List[str]
    video_url: Optional[AnyHttpUrl] = Field(None)
    location: str = Field(..., validation_alias="city")
    ethnographic_district: Optional[str]
    collectors: Optional[List[str]] = Field(None)
    performers: Optional[str] = Field(None)
    recording_date: date
    photos: Optional[List[AnyHttpUrl]] = Field(None)
    stereo_audio: Optional[str] = Field(None)
    multichannels: Optional[List[str]] = Field(None)
    fund: FundSchema

    @field_validator(
        "photos", "multichannels", "stereo_audio", "genres", "location", mode="before"
    )
    @classmethod
    def modify_fields(cls, value: str, info: ValidationInfo) -> str:
        match info.field_name:
            case "photos" | "multichannels":
                result = []
                for url in value:
                    if url:
                        result.append(f"{settings.BASE_URL}/{url}")
                return result
            case "stereo_audio":
                if value:
                    return f"{settings.BASE_URL}/{value}"
            case "genres":
                if value:
                    return [item.genre_name for item in value]
                return []
            case "location":
                return f"{value.name}, {value.region.name}, {value.country.name}"
