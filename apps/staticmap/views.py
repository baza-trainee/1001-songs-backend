from django.db.models import Count
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

from apps.songs.models import Song
from apps.songs.serializers import SongSerializer


class MapListView(GenericAPIView):
    """
    List of songs with cities, lists of cities and archives

    URL:
    - /map
    """

    queryset = Song.objects.all()
    serializer_class = SongSerializer

    @staticmethod
    @extend_schema(
        responses={
            200: OpenApiTypes.OBJECT
        },
        examples=[
            OpenApiExample(
                name="Example",
                description="Getting list of songs with cities, lists of cities and archives",
                value=[
                    {"list_markers": [{
                        "location__city_ua": "Київ",
                        "location__coordinates": "50.53619010179338, 30.62149563",
                        "count": 1
                    }]},

                    {"list_cities": [{
                        "location__city_ua": "Вінниця",
                        "location__city_eng": "Vinnitsa"
                    },]},

                    {"list_archives": [{
                        "archive_ua": "абц",
                        "archive_eng": "abc"
                    },]},
                ],
                response_only=True
            )
        ],
        methods=["GET"]
    )
    def get(*args, **kwargs):
        list_markers = (Song.objects.values('location__city_ua', 'location__coordinates')
                        .annotate(count=Count('location__city_ua')))
        list_cities = (Song.objects.order_by('location__city_ua').values('location__city_ua', 'location__city_eng')
                       .distinct('location__city_ua'))
        list_archives = (Song.objects.order_by('archive_ua').values('archive_ua', 'archive_eng')
                         .distinct('archive_ua'))
        return Response([
            {'list_markers': list_markers},
            {'list_cities': list_cities},
            {'list_archives': list_archives}
        ])


class MapCityListView(GenericAPIView):
    """
    List of songs in the selected city

    URL: /map/city?city_ua=city_ua
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    @extend_schema(
        parameters=[OpenApiParameter(
            name='city_ua',
            description='Need to pass the name of the city from the list of cities',
            required=False,
            type=str,
        )],
        methods=["GET"]
    )
    def get(self, *args, **kwargs):
        params = self.request.query_params.dict()
        if params:
            songs_city = Song.objects.filter(location__city_ua=params['city_ua'])
            serializer = SongSerializer(instance=songs_city, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('Specify the search city', status=status.HTTP_404_NOT_FOUND)
