from rest_framework.generics import ListAPIView

from apps.educational_section.models import EducationalSection
from apps.educational_section.serializers import EducationalSectionSerializer


class EducationalSectionListView(ListAPIView):
    """
    List of educational section
    """
    queryset = EducationalSection.objects.all()
    serializer_class = EducationalSectionSerializer
