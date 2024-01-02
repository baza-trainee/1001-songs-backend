from django_filters import rest_framework as filters

from .models import SongES


class SongESFilter(filters.FilterSet):
    class Meta:
        model = SongES
        fields = ('genre',)
    genre = filters.BaseInFilter(field_name='genre', lookup_expr='in')

