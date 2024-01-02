from django.urls import path

from apps.staticmap.views import MapListView, MapCityListView

urlpatterns = [
    path('', MapListView.as_view(), name='list_map'),
    path('/city', MapCityListView.as_view(), name='city_list_map'),
]


