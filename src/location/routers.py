from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_async_session
from .service import get_record, get_records
from .models import Country, Region, City
from .schemas import BaseLocation, RegionSchema, CitySchema


location_router = APIRouter(prefix="/location", tags=["Location"])


@location_router.get("/countries", response_model=List[BaseLocation])
async def get_countries(session: AsyncSession = Depends(get_async_session)):
    return await get_records(Country, session)


@location_router.get("/regions", response_model=List[RegionSchema])
async def get_regions(session: AsyncSession = Depends(get_async_session)):
    return await get_records(Region, session)


@location_router.get("/cities", response_model=List[CitySchema])
async def get_cities(session: AsyncSession = Depends(get_async_session)):
    return await get_records(City, session)


@location_router.get("/countries/{id}", response_model=List[RegionSchema])
async def get_regions_by_country_id(
    id: int, session: AsyncSession = Depends(get_async_session)
):
    return await get_record(Region, Region.country_id == id, session)


@location_router.get("/regions/{id}", response_model=List[CitySchema])
async def get_cities_by_region_id(
    id: int, session: AsyncSession = Depends(get_async_session)
):
    return await get_record(City, City.region_id == id, session)
