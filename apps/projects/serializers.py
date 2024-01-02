from rest_framework.serializers import ModelSerializer

from apps.projects.models import Project


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'title', 'date_event', 'photo_1',
        )


class ProjectByIdSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'title', 'date_event', 'brief_description', 'location', 'photo_1', 'text_1_intro',
            'photo_2', 'text_2', 'author', 'editor', 'svitliny',
        )
