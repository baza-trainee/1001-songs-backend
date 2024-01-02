from django.db.models import Count

from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response

from .models import Song
from .serializers import SongSerializer
from .filters import SongFilter


class SongsAndMarkersListView(GenericAPIView):
    """
    List of songs and markers
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filterset_class = SongFilter

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        list_markers = (queryset.values('location__city_ua', 'location__coordinates')
                        .annotate(count=Count('location__city_ua')))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response([{'list_songs': serializer.data}, {'list_markers': list_markers}])


class SongRetrieveByIdView(RetrieveAPIView):
    """
    Retrieve song by id
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer
