from django_filters import rest_framework as filters

from .models import Song


class SongFilter(filters.FilterSet):
    class Meta:
        model = Song
        fields = (
            'title', 'country', 'region', 'city_ua', 'city_eng', 'genre', 'archive_ua', 'archive_eng', 'coordinates',
        )
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    country = filters.BaseInFilter(field_name='location__country', lookup_expr='in')
    region = filters.BaseInFilter(field_name='location__region', lookup_expr='in')
    city_ua = filters.BaseInFilter(field_name='location__city_ua', lookup_expr='in')
    city_eng = filters.BaseInFilter(field_name='location__city_eng', lookup_expr='in')
    genre = filters.BaseInFilter(field_name='details__genre_cycle', lookup_expr='in')
    archive_ua = filters.BaseInFilter(field_name='archive_ua', lookup_expr='in')
    archive_eng = filters.BaseInFilter(field_name='archive_eng', lookup_expr='in')
    coordinates = filters.CharFilter(field_name='location__coordinates', lookup_expr='exact')
