from rest_framework.serializers import ModelSerializer

from apps.educational_section.models import EducationalSection


class EducationalSectionSerializer(ModelSerializer):
    class Meta:
        model = EducationalSection
        fields = (
            'id', 'title', 'description', 'photo1', 'photo2', 'photo3', 'photo4', 'photo5',
        )

