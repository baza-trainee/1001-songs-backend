from sqlalchemy.ext.asyncio import AsyncSession
from .models import Country, City, Region
from .exceptions import AFTER_COUNTRY_CREATE


async def create_countries(countries_list: list[dict], session: AsyncSession):
    try:
        for country in countries_list:
            instance = Country(**country)
            session.add(instance)
        print(AFTER_COUNTRY_CREATE)
    except Exception as exc:
        raise exc


async def create_regions(regions_list: list[dict], session: AsyncSession):
    try:
        for region in regions_list:
            instance = Region(**region)
            session.add(instance)
        print(AFTER_COUNTRY_CREATE)
    except Exception as exc:
        raise exc


async def create_city(city_list: list[dict], session: AsyncSession):
    try:
        for city in city_list:
            instance = City(**city)
            session.add(instance)
        print(AFTER_COUNTRY_CREATE)
    except Exception as exc:
        raise exc
