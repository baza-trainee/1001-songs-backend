from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import distinct, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate

from src.database.database import get_async_session
from src.exceptions import NO_DATA_FOUND
from src.song.models import Fund, Song, Genre
from .exceptions import (
    NO_FUND_FOUND,
    NO_GENRES_FOUND,
    NO_REGION_FOUND,
    NO_CITIES_FOUND,
    NO_SONG_FOUND,
)
from .models import Country, Region, City
from .schemas import (
    CountrySchema,
    GenreFilterSchema,
    RegionSchema,
    CitySchema,
    FilterSongSchema,
    FilterMapSchema,
    SongMapPageSchema,
    FundFilterSchema,
)


location_router = APIRouter(prefix="/location", tags=["Dropdowns"])
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
    country_id: List[int] = Query(None),
    genre_id: List[int] = Query(None),
    fund_id: List[int] = Query(None),
    city_id: List[int] = Query(None),
    session: AsyncSession = Depends(get_async_session),
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
                func.count(distinct(Song.id)).label("count"),
            )
            .join(City, Region.id == City.region_id)
            .join(Song)
            .group_by(Region.id)
            .order_by(Region.name)
        )

        if country_id:
            query = query.filter(Region.country_id.in_(country_id))
        if city_id:
            query = query.filter(City.id.in_(city_id))
        if genre_id:
            query = query.join(Song.genres).filter(Genre.id.in_(genre_id))
        if fund_id:
            query = query.filter(Song.fund_id.in_(fund_id))

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
    country_id: List[int] = Query(None),
    region_id: List[int] = Query(None),
    genre_id: List[int] = Query(None),
    fund_id: List[int] = Query(None),
    session: AsyncSession = Depends(get_async_session),
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

        if region_id:
            query = query.filter(City.region_id.in_(region_id))
        if country_id:
            query = query.filter(City.country_id.in_(country_id))
        if genre_id:
            query = query.filter(Song.genres.any(Genre.id.in_(genre_id)))
        if fund_id:
            query = query.filter(Song.fund_id.in_(fund_id))
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


@location_router.get("/genres", response_model=List[GenreFilterSchema])
async def get_genres(
    country_id: List[int] = Query(None),
    region_id: List[int] = Query(None),
    city_id: List[int] = Query(None),
    fund_id: List[int] = Query(None),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Use this endpoint to retrieve genres. You can filter them by country, region, or city by passing one or more IDs.
    """
    try:
        query = (
            select(Genre.id, Genre.genre_name, func.count(Song.id).label("count"))
            .join(Song.genres)
            .join(City, Song.city_id == City.id)
            .join(Region, City.region_id == Region.id)
            .join(Country, City.country_id == Country.id)
            .join(Fund, Song.fund_id == Fund.id)
            .group_by(Genre.id)
            .order_by(Genre.id)
        )

        if country_id:
            query = query.filter(Country.id.in_(country_id))
        if region_id:
            query = query.filter(Region.id.in_(region_id))
        if city_id:
            query = query.filter(City.id.in_(city_id))
        if fund_id:
            query = query.filter(Song.fund_id.in_(fund_id))

        records = await session.execute(query)
        result = records.all()
        if not result:
            raise NoResultFound
        return [
            {
                "id": record.id,
                "genre_name": record.genre_name,
                "song_count": record.count,
            }
            for record in result
        ]
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=NO_GENRES_FOUND,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@location_router.get("/funds", response_model=List[FundFilterSchema])
async def get_funds(
    country_id: List[int] = Query(None),
    region_id: List[int] = Query(None),
    city_id: List[int] = Query(None),
    genre_id: List[int] = Query(None),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        query = (
            select(Fund.id, Fund.title, func.count(Song.id).label("count"))
            .join(Song, Fund.id == Song.fund_id)
            .join(City, Song.city_id == City.id)
            .join(Region, City.region_id == Region.id)
            .join(Country, City.country_id == Country.id)
            .group_by(Fund.id)
            .order_by(Fund.id)
        )

        if country_id:
            query = query.filter(Country.id.in_(country_id))
        if region_id:
            query = query.filter(Region.id.in_(region_id))
        if city_id:
            query = query.filter(City.id.in_(city_id))
        if genre_id:
            query = query.join(Song.genres).filter(Genre.id.in_(genre_id))

        records = await session.execute(query)
        result = records.all()
        if not result:
            raise NoResultFound
        return [
            {
                "id": record.id,
                "fund_name": record.title,
                "song_count": record.count,
            }
            for record in result
        ]
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=NO_FUND_FOUND,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@map_router.get("/filter/songs", response_model=Page[FilterSongSchema])
async def filter_songs(
    search: Optional[str] = Query(None),
    country_ids: List[int] = Query(None),
    region_ids: List[int] = Query(None),
    city_ids: List[int] = Query(None),
    genre_ids: List[int] = Query(None),
    fund_ids: List[int] = Query(None),
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
        if fund_ids:
            query = query.filter(Song.fund_id.in_(fund_ids))
        if genre_ids:
            query = query.join(Song.genres).filter(Genre.id.in_(genre_ids))
        if search:
            query = query.filter(Song.title.ilike(f"%{search}%"))

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


@map_router.get("/filter/geotag", response_model=List[FilterMapSchema])
async def filter_song_geotags(
    search: Optional[str] = Query(None),
    country_ids: List[int] = Query(None),
    region_ids: List[int] = Query(None),
    city_ids: List[int] = Query(None),
    genre_ids: List[int] = Query(None),
    fund_ids: List[int] = Query(None),
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
        if fund_ids:
            query = query.filter(Song.fund_id.in_(fund_ids))
        if genre_ids:
            query = query.join(Song.genres).filter(Genre.id.in_(genre_ids))
        if search:
            query = query.filter(Song.title.ilike(f"%{search}%"))

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


@map_router.get("/filter/songs/{id}", response_model=SongMapPageSchema)
async def get_song_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Accepts the song `ID` and returns detailed information about it.
    """
    try:
        record = await session.get(Song, id)
        if not record:
            raise NoResultFound
        return record
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
