from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
from src.database.database import get_async_session
from src.exceptions import NO_DATA_FOUND, SERVER_ERROR
from .models import (
    EducationPage,
    CalendarAndRitualCategory,
    EducationPageSongGenre,
    SongSubcategory,
)
from .schemas import EducationSchema, CategorySchema, EducationGenreSchema, SongSchema


education_router = APIRouter(prefix="/education", tags=["Education"])


@education_router.get("", response_model=EducationSchema)
async def get_education_page(session: AsyncSession = Depends(get_async_session)):
    """
    This endpoint returns information for the education section page.\n
    It includes an array of main song categories,
    each element of which contains an `ID` **that needs to be used subsequently to retrieve a specific section**.
    """
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
    """
    Accepts the **`ID` of one of the main categories** and returns more detailed information about the category. \n
    The output also includes lists of subcategories, each of which aggregates its respective genres.
    Each genre contains an 'id' field, which is used to obtain more detailed information about each of them in endpoints such as:
    - ```api/v1/education/genre/{id}```\n
    - ```api/v1/education/genre/{id}/songs```
    """
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
async def get_genre_info(id: int, session: AsyncSession = Depends(get_async_session)):
    """Accepts the genre `ID` and returns detailed **information about it**."""
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


@education_router.get("/genre/{id}/songs", response_model=List[SongSchema])
async def get_songs_by_education_genre(
    id: int, session: AsyncSession = Depends(get_async_session)
):
    """Accepts the genre `ID` and returns the corresponding **list of songs**."""
    try:
        genre = await session.get(EducationPageSongGenre, id)
        if not (genre and genre.songs):
            raise NoResultFound
        response = [
            {
                "id": song.id,
                "title": song.title,
                "photos": [photo for photo in song.photos if photo is not None],
                "stereo_audio": song.stereo_audio,
                "recording_location": song.recording_location,
                "genres": {"id": genre.id, "title": genre.title},
            }
            for song in genre.songs
        ]
        return response
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
