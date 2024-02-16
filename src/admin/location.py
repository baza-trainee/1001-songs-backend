from sqladmin import ModelView
from sqladmin.ajax import QueryAjaxModelLoader
from sqladmin.fields import AjaxSelectField, QuerySelectField, Select2TagsField
from wtforms.validators import DataRequired

from src.location.models import City, Country, Region


class CountryAdmin(ModelView, model=Country):
    is_async = True

    category = "Локації"
    name_plural = "Країни"
    icon = "fa-solid fa-earth-europe"

    can_edit = True
    can_create = True
    can_export = False

    column_list = [
        Country.name,
    ]
    column_labels = {
        Country.name: "Країна",
        Country.regions: "Області",
        Country.cities: "Міста та поселення",
    }
    form_excluded_columns = [
        Country.regions,
        Country.cities,
    ]
    column_details_list = [
        Country.name,
        Country.regions,
        Country.cities,
    ]


class RegionAdmin(ModelView, model=Region):
    is_async = True

    category = "Локації"
    name_plural = "Області та регіони"
    icon = "fa-solid fa-map-location-dot"

    can_edit = True
    can_create = True
    can_delete = True
    can_export = False

    column_list = [
        Region.name,
    ]
    column_list = [
        Region.name,
        Region.country,
    ]
    column_labels = {
        Region.name: "Область",
        Region.country: "Країна",
        Region.cities: "Міста / Поселення",
    }
    column_details_list = [
        Region.country,
        Region.name,
        Region.cities,
    ]
    form_excluded_columns = [
        Region.cities,
    ]

    form_ajax_refs = {
        "country": {
            "fields": ("name",),
            "order_by": "id",
        },
    }


class CityAdmin(ModelView, model=City):
    is_async = True

    category = "Локації"
    name_plural = "Міста та поселення"
    icon = "fa-solid fa-location-dot"

    can_edit = True
    can_create = True
    can_delete = True

    column_list = [
        City.country,
        City.region,
        City.name,
        City.latitude,
        City.longitude,
    ]
    column_labels = {
        City.country: "Країна",
        City.region: "Область",
        City.name: "Населений пункт",
        City.latitude: "Широта",
        City.longitude: "Довгота",
    }
    column_details_list = [
        City.country,
        City.region,
        City.name,
        City.latitude,
        City.longitude,
    ]
    form_columns = [
        City.country,
        City.region,
        City.name,
        City.latitude,
        City.longitude,
    ]
    form_args = {
        "country": {
            "validators": [DataRequired()],
        },
        "region": {
            "validators": [DataRequired()],
        },
        "latitude": {
            "validators": [DataRequired()],
        },
        "longitude": {
            "validators": [DataRequired()],
        },
    }

    form_ajax_refs = {
        "country": {
            "fields": ("name",),
            "order_by": "id",
        },
        "region": {
            "fields": ("name",),
            "order_by": "id",
        },
    }
