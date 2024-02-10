from sqladmin import ModelView
from src.location.models import City, Country, Region


class CountryAdmin(ModelView, model=Country):
    column_list = [Country.name]
    can_edit = True
    can_create = True
    category = "Location"


class RegionAdmin(ModelView, model=Region):
    column_list = [Region.name]
    can_edit = True
    can_create = True
    can_delete = True
    category = "Location"


class CityAdmin(ModelView, model=City):
    column_list = [City.name, City.latitude, City.longitude]
    can_edit = True
    can_create = True
    can_delete = True
    category = "Location"
