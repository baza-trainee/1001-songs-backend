from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound

from src.database.database import get_async_session
from src.exceptions import NO_DATA_FOUND, SERVER_ERROR
from .models import EducationSection
from .schemas import EducationSchema


education_router = APIRouter(prefix="/education", tags=["Education"])


@education_router.get("", response_model=List[EducationSchema])
async def get_education_list(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(EducationSection).order_by("id")
        story = await session.execute(query)
        response = story.scalars().all()
        if not response:
            raise NoResultFound
        return response
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SERVER_ERROR
        )


@education_router.get("/{id}", response_model=EducationSchema)
async def get_education(id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        record = await session.get(EducationSection, id)
        if not record:
            raise NoResultFound
        return record
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SERVER_ERROR
        )
