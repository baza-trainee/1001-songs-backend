from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.expeditions.models import Expedition
from apps.expeditions.serializers import ExpeditionSerializer, ExpeditionByIdSerializer


class ExpeditionListView(ListAPIView):
    """
    List of expeditions
    """
    queryset = Expedition.objects.all()
    serializer_class = ExpeditionSerializer


class ExpeditionRetrieveView(RetrieveAPIView):
    """
    Retrieve expedition by id
    """
    queryset = Expedition.objects.all()
    serializer_class = ExpeditionByIdSerializer
