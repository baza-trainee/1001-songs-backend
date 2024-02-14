from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate

from src.database.database import get_async_session
from src.song.models import Song, Genre
from .exceptions import NO_REGION_FOUND, NO_CITIES_FOUND, NO_SONG_FOUND
from .models import Country, Region, City
from .schemas import (
    CountrySchema,
    RegionSchema,
    CitySchema,
    FilterSongSchema,
    FilterMapSchema,
)


location_router = APIRouter(prefix="/location", tags=["Dropdown locations"])
map_router = APIRouter(prefix="/map", tags=["Map"])


@location_router.get("/countries", response_model=List[CountrySchema])
async def get_countries(session: AsyncSession = Depends(get_async_session)):
    query = (
        select(Country.id, Country.name, func.count(Song.id).label("count"))
        .join(Region)
        .join(City)
        .join(Song)
        .group_by(Country.id)
        .order_by(Country.name)
    )
    records = await session.execute(query)
    result = records.all()
    return [
        {
            "id": record.id,
            "name": record.name,
            "song_count": record.count,
        }
        for record in result
    ]


@location_router.get("/regions", response_model=List[RegionSchema])
async def get_regions(
    id: List[int] = Query(None), session: AsyncSession = Depends(get_async_session)
):
    """
    Use this endpoint to retrieve regions. You can filter them by country by passing one or more **country ID**s.
    """
    try:
        query = (
            select(
                Region.id,
                Region.name,
                Region.country_id,
                func.count(Song.id).label("count"),
            )
            .join(City, Region.id == City.region_id)
            .join(Song)
            .group_by(Region.id)
            .order_by(Region.name)
        )

        if id:
            query = query.filter(Region.country_id.in_(id))

        records = await session.execute(query)
        result: List[Region] = records.all()
        if not result:
            raise NoResultFound
        return [
            {
                "id": record.id,
                "name": record.name,
                "country_id": record.country_id,
                "song_count": record.count,
            }
            for record in result
        ]
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
    id: List[int] = Query(None), session: AsyncSession = Depends(get_async_session)
):
    """
    Use this endpoint to retrieve cities. You can filter them by region by passing one or more **region ID**s.
    """
    try:
        query = (
            select(
                City.id,
                City.name,
                City.country_id,
                City.region_id,
                func.count(Song.id).label("count"),
            )
            .join(Song, City.id == Song.city_id)
            .group_by(City.id)
            .order_by(City.name)
        )

        if id:
            query = query.filter(City.region_id.in_(id))

        records = await session.execute(query)
        result = records.all()
        if not result:
            raise NoResultFound
        return [
            {
                "id": record.id,
                "name": record.name,
                "song_count": record.count,
                "country_id": record.country_id,
                "region_id": record.region_id,
            }
            for record in result
        ]
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=NO_CITIES_FOUND,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@map_router.get("/filter-song", response_model=Page[FilterSongSchema])
async def filter_songs(
    country_ids: List[int] = Query(None),
    region_ids: List[int] = Query(None),
    city_ids: List[int] = Query(None),
    genre_ids: List[int] = Query(None),
    session: AsyncSession = Depends(get_async_session),
):
    """Use this endpoint to filter songs by country, region, city, and genre. Endpoint returns paginated elements."""
    try:
        query = select(Song).join(City).join(Region).join(Country).order_by(Song.id)

        if country_ids:
            query = query.filter(Country.id.in_(country_ids))
        if region_ids:
            query = query.filter(Region.id.in_(region_ids))
        if city_ids:
            query = query.filter(City.id.in_(city_ids))
        if genre_ids:
            query = query.join(Song.genres).filter(Genre.id.in_(genre_ids))

        result = await paginate(session, query)
        if not result.items:
            raise NoResultFound
        return result
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=NO_SONG_FOUND,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@map_router.get("/filter-geotag", response_model=List[FilterMapSchema])
async def filter_song_geotags(
    country_ids: List[int] = Query(None),
    region_ids: List[int] = Query(None),
    city_ids: List[int] = Query(None),
    genre_ids: List[int] = Query(None),
    session: AsyncSession = Depends(get_async_session),
):
    """Use this endpoint to filter geotag by Country, Region, City, or Genre. Or all at once."""
    try:
        query = (
            select(
                City.id.label("id"),
                City.name,
                City.latitude,
                City.longitude,
                Region.name.label("region_name"),
                func.count(Song.id).label("count"),
            )
            .join(Song)
            .join(Region)
            .join(Country)
            .group_by(City.id, Region.name)
            .order_by(City.id)
        )

        if country_ids:
            query = query.filter(Country.id.in_(country_ids))
        if region_ids:
            query = query.filter(Region.id.in_(region_ids))
        if city_ids:
            query = query.filter(City.id.in_(city_ids))
        if genre_ids:
            query = query.join(Song.genres).filter(Genre.id.in_(genre_ids))

        records = await session.execute(query)
        result = records.all()
        if not result:
            raise NoResultFound
        return [
            {
                "id": record.id,
                "city": f"{record.name}, {record.region_name}",
                "latitude": record.latitude,
                "longitude": record.longitude,
                "count": record.count,
            }
            for record in result
        ]
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=NO_SONG_FOUND,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
