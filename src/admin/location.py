from sqladmin import ModelView
from src.location.models import City, Country, Region


class CountryAdmin(ModelView, model=Country):
    icon = "fa-solid fa-earth-europe"
    column_list = [Country.name]
    can_edit = True
    can_create = True
    can_export = False
    category = "Локації"
    name_plural = "Країни"

    column_labels = {
        Country.name: "Країна",
        Country.cities: "Міста та селища",
        Country.regions: "Області",
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
    icon = "fa-solid fa-map-location-dot"
    column_list = [Region.name]
    can_edit = True
    can_create = True
    can_delete = True
    can_export = False
    category = "Локації"
    name_plural = "Області та регіони"

    column_list = [
        Region.name,
        Region.country,
    ]
    column_labels = {
        Region.name: "Область",
        Region.country: "Країна",
        Region.cities: "Міста / Поселення",
    }
    form_excluded_columns = [
        Region.cities,
    ]
    column_details_list = [
        Region.country,
        Region.name,
        Region.cities,
    ]


class CityAdmin(ModelView, model=City):
    icon = "fa-solid fa-location-dot"
    column_list = [City.name, City.latitude, City.longitude]
    can_edit = True
    can_create = True
    can_delete = True
    category = "Локації"
    name_plural = "Міста та поселення"

    column_list = [
        City.name,
        City.region,
        City.country,
    ]
    column_labels = {
        City.country: "Країна",
        City.region: "Область",
        City.name: "Населений пункт",
        City.latitude: "Широта",
        City.longitude: "Довгота",
    }
    form_excluded_columns = [City.country]
    column_details_list = [
        City.country,
        City.region,
        City.name,
        City.latitude,
        City.longitude,
    ]
