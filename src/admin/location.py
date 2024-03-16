from typing import Any

from fastapi import Request
from sqlalchemy import select
from wtforms import ValidationError
from wtforms.validators import DataRequired

from src.admin.commons.base import BaseAdmin
from src.database.redis import invalidate_cache_partial
from src.location.models import City, Country, Region


class CountryAdmin(BaseAdmin, model=Country):
    category = "Локації"
    name_plural = "Країни"
    icon = "fa-solid fa-earth-europe"
    can_view_details = True

    column_list = form_columns = column_details_list = [
        Country.name,
    ]
    column_labels = {
        Country.name: "Країна",
    }
    column_searchable_list = [
        Country.name,
    ]

    async def delete_model(self, request: Request, pk: Any) -> None:
        stmt = select(self.model).filter_by(id=int(pk))
        records = await self._run_query(stmt)
        if records:
            regions = records[0].regions
            if regions:
                message = f"Неможливо видалити країну <b>{records[0]}</b>"
                message += f", оскільки з нею пов'язані регіони: <b>{', '.join(map(str, regions))}</b>."
                return {"error_message": message}
        return await super().delete_model(request, pk)


class RegionAdmin(BaseAdmin, model=Region):
    category = "Локації"
    name_plural = "Області та регіони"
    icon = "fa-solid fa-map-location-dot"
    can_view_details = True

    column_list = form_columns = [
        Region.country,
        Region.name,
    ]
    column_labels = {
        Region.country: "Країна",
        Region.name: "Область / Регіон",
        Region.cities: "Міста / Поселення",
    }
    column_details_list = [
        Region.country,
        Region.name,
    ]
    column_searchable_list = [
        Region.name,
    ]
    form_args = {
        "country": {
            "validators": [DataRequired()],
        },
    }
    form_ajax_refs = {
        "country": {
            "fields": ("name",),
            "order_by": "name",
        },
    }
    column_searchable_list = [
        Region.name,
    ]

    async def delete_model(self, request: Request, pk: Any) -> None:
        stmt = select(self.model).filter_by(id=int(pk))
        records = await self._run_query(stmt)
        if records:
            cities = records[0].cities
            if cities:
                cities = [city.name for city in cities]
                message = f"Неможливо видалити регіон <b>{records[0]}</b>"
                message += (
                    f", оскільки з ним пов'язані міста: <b>{', '.join(cities)}</b>."
                )
                return {"error_message": message}
        return await super().delete_model(request, pk)


class CityAdmin(BaseAdmin, model=City):
    category = "Локації"
    name_plural = "Міста та поселення"
    icon = "fa-solid fa-location-dot"
    can_view_details = True

    column_labels = {
        City.region: "Область / Регіон",
        City.name: "Місто / Поселення",
        City.latitude: "Широта",
        City.longitude: "Довгота",
        City.administrative_code: "Адміністративний код",
    }
    column_list = column_details_list = form_columns = [
        City.region,
        City.name,
        City.latitude,
        City.longitude,
        City.administrative_code,
    ]
    column_searchable_list = [
        City.name,
        City.administrative_code,
    ]
    form_args = {
        "administrative_code": {"validators": [DataRequired()]},
        "region": {
            "validators": [DataRequired()],
        },
    }
    form_ajax_refs = {
        "region": {
            "fields": ("name",),
            "order_by": "name",
        },
    }

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        model.country_id = model.region.country_id
        stmt = select(self.model.administrative_code).filter_by(
            administrative_code=data["administrative_code"]
        )
        records = await self._run_query(stmt)
        if records and model.administrative_code not in records:
            raise ValidationError(message="Administrative code must be unique.")
        return await super().on_model_change(data, model, is_created, request)

    async def after_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        await invalidate_cache_partial(["filter_song_geotags"])
        return await super().after_model_change(data, model, is_created, request)

    async def after_model_delete(self, model: Any, request: Request) -> None:
        await invalidate_cache_partial(["filter_song_geotags"])
        return await super().after_model_delete(model, request)

    async def delete_model(self, request: Request, pk: Any) -> None:
        stmt = select(self.model).filter_by(id=int(pk))
        records = await self._run_query(stmt)
        if records:
            message = f"Неможливо видалити місто <b>{records[0]}</b>, оскільки з ним пов'язані:"
            songs = records[0].songs
            expeditions = records[0].expeditions
            news = records[0].news
            projects = records[0].projects
            if songs:
                message += f"<br>пісні: <b>{', '.join(map(str, songs))}</b>."
            if expeditions:
                message += f"<br>експедиції: <b>{', '.join(map(str, expeditions))}</b>."
            if news:
                message += f"<br>новини: <b>{', '.join(map(str, news))}</b>."
            if projects:
                message += f"<br>проєкти: <b>{', '.join(map(str, projects))}</b>."
            if songs or expeditions or news or projects:
                return {"error_message": message}
        return await super().delete_model(request, pk)
