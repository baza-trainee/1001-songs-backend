from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from src.database.database import get_async_session
from src.exceptions import NO_DATA_FOUND, SERVER_ERROR
from .exceptions import NO_REGION_FOUND
from .models import Country, Region


location_router = APIRouter(prefix="/location", tags=["Location"])


@location_router.get("/countries")
async def get_countries(session: AsyncSession = Depends(get_async_session)):
    try:
        records = await session.execute(select(Country))
        result = records.scalars().all()
        if not result:
            raise NoResultFound
        return result
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SERVER_ERROR
        )


@location_router.get("/countries/{country_id}/regions")
async def get_regions_by_country_id(
    country_id: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        records = await session.execute(
            select(Region).where(Region.country_id == country_id)
        )
        result = records.scalars().all()
        if not result:
            raise NoResultFound
        return result
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=NO_REGION_FOUND % country_id,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SERVER_ERROR
        )
