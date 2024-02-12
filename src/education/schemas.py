from typing import List, Optional

from pydantic import BaseModel, Field, AnyHttpUrl, ValidationInfo, field_validator

from src.config import settings
from .models import EducationPage


TITLE_LEN = EducationPage.title.type.length
DESCRIPTION_LEN = EducationPage.description.type.length
RECOMENDATIONS_LEN = EducationPage.recommendations.type.length
SOURCES_LEN = EducationPage.recommended_sources.type.length


class BaseCycleSchema(BaseModel):
    id: int = Field(..., ge=1)
    title: str = Field(..., max_length=TITLE_LEN)
    media: Optional[AnyHttpUrl] = Field(None)


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
