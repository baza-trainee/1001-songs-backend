from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import distinct, func, select
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


location_router = APIRouter(prefix="/filter", tags=["Dropdowns"])
map_router = APIRouter(prefix="/map", tags=["Map"])


@location_router.get("/location/countries", response_model=List[CountrySchema])
async def get_countries(
    city_id: List[int] = Query(None),
    region_id: List[int] = Query(None),
    genre_id: List[int] = Query(None),
    fund_id: List[int] = Query(None),
    session: AsyncSession = Depends(get_async_session),
):
    """Use this endpoint to retrieve a list of countries where songs are available. You can filter the countries based on specific criteria such as city, region, genre, or fund by providing the following query parameters:

    - **city_id**: Filter countries by the **ID**(s) of the city or cities where songs are available.
    - **region_id**: Filter countries by the **ID**(s) of the region or regions where songs are available.
    - **genre_id**: Filter countries by the **ID**(s) of the genre or genres of available songs.
    - **fund_id**: Filter countries by the **ID**(s) of the fund or funds supporting available songs.

    The endpoint returns a list of countries, each containing the following information:
    - **id** (int): The unique identifier of the country.
    - **name** (str): The name of the country.
    - **song_count** (int): The number of songs available in the country that meet the specified criteria.
    """
    try:
        query = (
            select(
                Country.id, Country.name, func.count(distinct(Song.id)).label("count")
            )
            .join(Region)
            .join(City)
            .join(Song)
            .group_by(Country.id)
            .order_by(Country.name)
        )

        if city_id:
            query = query.filter(City.id.in_(city_id))
        if region_id:
            query = query.filter(City.region_id.in_(region_id))
        if fund_id:
            query = query.filter(Song.fund_id.in_(fund_id))
        if genre_id:
            query = query.join(Song.genres).filter(Genre.id.in_(genre_id))

        records = await session.execute(query)
        result = records.all()
        if not result:
            raise NoResultFound
        return [
            {
                "id": record.id,
                "name": record.name,
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


@location_router.get("/location/regions", response_model=List[RegionSchema])
async def get_regions(
    country_id: List[int] = Query(None),
    city_id: List[int] = Query(None),
    genre_id: List[int] = Query(None),
    fund_id: List[int] = Query(None),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Use this endpoint to retrieve a list of regions. You can filter them by country, city, genre, or fund by providing the following query parameters:

    - **country_id**: Filter regions by the **ID**(s) of the country or countries to which they belong.
    - **city_id**: Filter regions by the **ID**(s) of the city or cities within the regions.
    - **genre_id**: Filter regions by the **ID**(s) of the genre or genres of available songs within the regions.
    - **fund_id**: Filter regions by the **ID**(s) of the fund or funds supporting available songs within the regions.

    The endpoint returns a list of regions, each containing the following information:
    - **id** (int): The unique identifier of the region.
    - **name** (str): The name of the region.
    - **country_id** (int): The ID of the country to which the region belongs.
    - **song_count** (int): The number of songs available in the region that meet the specified criteria.
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


@location_router.get("/location/cities", response_model=List[CitySchema])
async def get_cities(
    country_id: List[int] = Query(None),
    region_id: List[int] = Query(None),
    genre_id: List[int] = Query(None),
    fund_id: List[int] = Query(None),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Use this endpoint to retrieve a list of cities. You can filter them by region, country, genre, or fund by providing the following query parameters:

    - **region_id**: Filter cities by the **ID**(s) of the region or regions to which they belong.
    - **country_id**: Filter cities by the **ID**(s) of the country or countries to which they belong.
    - **genre_id**: Filter cities by the **ID**(s) of the genre or genres of available songs within the cities.
    - **fund_id**: Filter cities by the **ID**(s) of the fund or funds supporting available songs within the cities.

    The endpoint returns a list of cities, each containing the following information:
    - **id** (int): The unique identifier of the city.
    - **name** (str): The name of the city.
    - **song_count** (int): The number of songs available in the city that meet the specified criteria.
    - **country_id** (int): The ID of the country to which the city belongs.
    - **region_id** (int): The ID of the region to which the city belongs.
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


@location_router.get("/song/genres", response_model=List[GenreFilterSchema])
async def get_genres(
    country_id: List[int] = Query(None),
    region_id: List[int] = Query(None),
    city_id: List[int] = Query(None),
    fund_id: List[int] = Query(None),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Use this endpoint to retrieve genres of songs. You can filter them by country, region, or city by passing one or more IDs.

    Parameters:
    - **country_id**: Filter genres by the ID(s) of the country or countries where songs are available.
    - **region_id**: Filter genres by the ID(s) of the region or regions where songs are available.
    - **city_id**: Filter genres by the ID(s) of the city or cities where songs are available.
    - **fund_id**: Filter genres by the ID(s) of the fund or funds supporting available songs.

    Returns:
    - A list of genres, each containing the following information:
        - **id** (int): The unique identifier of the genre.
        - **genre_name** (str): The name of the genre.
        - **song_count** (int): The number of songs available within the specified criteria.

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


@location_router.get("/song/funds", response_model=List[FundFilterSchema])
async def get_funds(
    country_id: List[int] = Query(None),
    region_id: List[int] = Query(None),
    city_id: List[int] = Query(None),
    genre_id: List[int] = Query(None),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Use this endpoint to retrieve funds supporting songs. You can filter them by country, region, city, or genre by passing one or more IDs.

    - **country_id**: Filter funds by the **ID**(s) of the country or countries where songs are supported.
    - **region_id**: Filter funds by the **ID**(s) of the region or regions where songs are supported.
    - **city_id**: Filter funds by the **ID**(s) of the city or cities where songs are supported.
    - **genre_id**: Filter funds by the **ID**(s) of the genre or genres of songs supported by the funds.

    Returns:
    - A list of funds, each containing the following information:
        - **id** (int): The unique identifier of the fund.
        - **fund_name** (str): The name of the fund.
        - **song_count** (int): The number of songs supported by the fund within the specified criteria.
    """
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
    country_id: List[int] = Query(None),
    region_id: List[int] = Query(None),
    city_id: List[int] = Query(None),
    genre_id: List[int] = Query(None),
    fund_id: List[int] = Query(None),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Use this endpoint to filter songs by country, region, city, genre, and fund. The endpoint accumulates all filters used by the user and returns a paginated list of songs that meet the specified criteria.

    Parameters:
    - **search**: Search query to filter songs by title.
    - **country_id**: Filter songs by the ID(s) of the country or countries where they are available.
    - **region_id**: Filter songs by the ID(s) of the region or regions where they are available.
    - **city_id**: Filter songs by the ID(s) of the city or cities where they are available.
    - **genre_id**: Filter songs by the ID(s) of the genre or genres.
    - **fund_id**: Filter songs by the ID(s) of the fund or funds supporting them.

    Returns:
    -  A paginated list of songs, each containing the following information:

    Note:
    - If no songs match the specified criteria, a 404 Not Found status code will be returned.
    - If an internal server error occurs during processing, a 500 Internal Server Error status code will be returned.
    """
    try:
        query = select(Song).join(City).join(Region).join(Country).order_by(Song.id)

        if country_id:
            query = query.filter(Country.id.in_(country_id))
        if region_id:
            query = query.filter(Region.id.in_(region_id))
        if city_id:
            query = query.filter(City.id.in_(city_id))
        if fund_id:
            query = query.filter(Song.fund_id.in_(fund_id))
        if genre_id:
            query = query.join(Song.genres).filter(Genre.id.in_(genre_id))
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
    country_id: List[int] = Query(None),
    region_id: List[int] = Query(None),
    city_id: List[int] = Query(None),
    genre_id: List[int] = Query(None),
    fund_id: List[int] = Query(None),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Use this endpoint to filter geotags by country, region, city, genre, or fund. You can apply multiple filters simultaneously.

    Parameters:
    - **search**: Search query to filter geotags by song title.
    - **country_id**: Filter geotags by the ID(s) of the country or countries.
    - **region_id**: Filter geotags by the ID(s) of the region or regions.
    - **city_id**: Filter geotags by the ID(s) of the city or cities.
    - **genre_id**: Filter geotags by the ID(s) of the genre or genres.
    - **fund_id**: Filter geotags by the ID(s) of the fund or funds supporting songs.

    Returns:
    - List: A list of geotags, each containing the following information:
        - **id** (int): The unique identifier of the city.
        - **city** (str): The name of the city along with its region name.
        - **latitude** (float): The latitude coordinate of the city.
        - **longitude** (float): The longitude coordinate of the city.
        - **song_count** (int): The number of songs available in the city that meet the specified criteria.

    Note:
    - If no geotags match the specified criteria, a 404 Not Found status code will be returned.
    - If an internal server error occurs during processing, a 500 Internal Server Error status code will be returned.
    """
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

        if country_id:
            query = query.filter(Country.id.in_(country_id))
        if region_id:
            query = query.filter(Region.id.in_(region_id))
        if city_id:
            query = query.filter(City.id.in_(city_id))
        if fund_id:
            query = query.filter(Song.fund_id.in_(fund_id))
        if genre_id:
            query = query.join(Song.genres).filter(Genre.id.in_(genre_id))
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
                "song_count": record.count,
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
