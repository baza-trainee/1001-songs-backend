from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound

from src.database.database import get_async_session
from src.exceptions import NO_DATA_FOUND, SERVER_ERROR
from .models import (
    EducationPage,
    CalendarAndRitualCategory,
    EducationPageSongGenre,
    SongSubcategory,
)
from .schemas import EducationSchema, CategorySchema, EducationGenreSchema


education_router = APIRouter(prefix="/education", tags=["Education"])


@education_router.get("", response_model=EducationSchema)
async def get_education_page(session: AsyncSession = Depends(get_async_session)):
    try:
        record = await session.get(EducationPage, 1)
        if not record:
            raise NoResultFound
        query = select(CalendarAndRitualCategory)
        categories_result = await session.execute(query)
        categories = categories_result.scalars().all()
        return {
            **record.__dict__,
            "calendar_and_ritual_categories": [
                {"id": category.id, "title": category.title, "media": category.media}
                for category in categories
            ],
        }
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@education_router.get("/category/{id}", response_model=CategorySchema)
async def get_category(id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        record = await session.get(CalendarAndRitualCategory, id)
        if not record:
            raise NoResultFound
        song_subcategories = [
            {
                "id": subcategory.id,
                "title": subcategory.title,
                "media": subcategory.media,
                "education_genres": [
                    {"id": genre.id, "title": genre.title}
                    for genre in subcategory.education_genres
                ],
            }
            for subcategory in record.song_subcategories
        ]
        return {
            **record.__dict__,
            "song_subcategories": song_subcategories,
        }
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@education_router.get("/genre/{id}", response_model=EducationGenreSchema)
async def get_songs_by_education_genre(
    id: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        record = await session.get(EducationPageSongGenre, id)
        if not record:
            raise NoResultFound
        return record
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
