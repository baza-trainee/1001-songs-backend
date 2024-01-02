from rest_framework.generics import ListAPIView, RetrieveAPIView

from .filters import SongESFilter
from .models import SongES
from .serializers import SongESSerializer


class SongESListView(ListAPIView):
    queryset = SongES.objects.all()
    serializer_class = SongESSerializer
    filterset_class = SongESFilter


class SongESRetrieveView(RetrieveAPIView):
    queryset = SongES.objects.all()
    serializer_class = SongESSerializer
