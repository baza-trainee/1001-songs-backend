from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate

from src.database.database import get_async_session
from src.exceptions import NO_DATA_FOUND
from src.song.models import Song, Genre
from .exceptions import NO_GENRES_FOUND, NO_REGION_FOUND, NO_CITIES_FOUND, NO_SONG_FOUND
from .models import Country, Region, City
from .schemas import (
    CountrySchema,
    GenreFilterSchema,
    RegionSchema,
    CitySchema,
    FilterSongSchema,
    FilterMapSchema,
    SongMapPageSchema,
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
    country_id: List[int] = Query(None),
    region_id: List[int] = Query(None),
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
            .group_by(Genre.id)
            .order_by(Genre.id)
        )

        if country_id:
            query = query.filter(Country.id.in_(country_id))
        if region_id:
            query = query.filter(Region.id.in_(region_id))
        if city_id:
            query = query.filter(City.id.in_(city_id))

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


@map_router.get("/filter/songs", response_model=Page[FilterSongSchema])
async def filter_songs(
    search: Optional[str] = Query(None),
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
        song = await session.get(Song, id)
        if not song:
            raise NoResultFound
        city: City = song.city
        region: Region = city.region
        country: Country = city.country
        location = f"{city.name}, {region.name}, {country.name}"
        song_info = {
            "id": song.id,
            "title": song.title,
            "song_text": song.song_text,
            "genres": [genre.genre_name for genre in song.genres],
            "video_url": song.video_url,
            "location": location,
            "ethnographic_district": song.ethnographic_district,
            "collectors": song.collectors,
            "performers": song.performers,
            "recording_date": song.recording_date,
            "photos": [photo for photo in song.photos if photo is not None],
            "stereo_audio": song.stereo_audio,
            "multichannels": [
                channel for channel in song.multichannels if channel is not None
            ],
        }
        return song_info
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
