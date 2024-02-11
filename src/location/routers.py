from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_async_session
from src.exceptions import SERVER_ERROR
from src.location.exceptions import NO_REGION_FOUND, NO_CITIES_FOUND
from .service import get_records
from .models import Country, Region, City
from .schemas import BaseLocation, RegionSchema, CitySchema
from sqlalchemy.orm.exc import NoResultFound

location_router = APIRouter(prefix="/location", tags=["Location"])


@location_router.get("/countries", response_model=List[BaseLocation])
async def get_countries(session: AsyncSession = Depends(get_async_session)):
    return await get_records(Country, session)


@location_router.get("/regions", response_model=List[RegionSchema])
async def get_regions(
    id: List[int] = Query(
        None, description="Press the button to add a field for a new ID"
    ),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Use this endpoint to retrieve regions. You can filter them by country by passing one or more **country ID**s.
    """
    try:
        if id:
            records = await session.execute(
                select(Region).filter(Region.country_id.in_(id))
            )
        else:
            records = await session.execute(select(Region))
        result = records.scalars().all()
        if not result:
            raise NoResultFound
        return result
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=NO_REGION_FOUND,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@location_router.get("/cities", response_model=List[CitySchema])
async def get_cities(
    id: List[int] = Query(
        None, description="Press the button to add a field for a new ID"
    ),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Use this endpoint to retrieve cities. You can filter them by region by passing one or more **region ID**s.
    """
    try:
        if id:
            records = await session.execute(select(City).filter(City.region_id.in_(id)))
        else:
            records = await session.execute(select(City))
        result = records.scalars().all()
        if not result:
            raise NoResultFound
        return result
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=NO_CITIES_FOUND,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
