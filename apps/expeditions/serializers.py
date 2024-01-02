from rest_framework.serializers import ModelSerializer

from apps.expeditions.models import Expedition


class ExpeditionSerializer(ModelSerializer):
    class Meta:
        model = Expedition
        fields = (
            'title', 'date_event', 'brief_description', 'location',
        )


class ExpeditionByIdSerializer(ModelSerializer):
    class Meta:
        model = Expedition
        fields = (
            'id', 'title', 'date_event', 'brief_description', 'location', 'type_expedition', 'coordinates',
            'text_1', 'video_1', 'text_2', 'text_3', 'text_4', 'text_5', 'photo', 'comment_to_photo', 'text_6',
            'video_2', 'comment_to_video_2', 'text_7', 'video_3', 'comment_to_video_3', 'text_8', 'video_4',
            'comment_to_video_4', 'text_9', 'text_10', 'collectors', 'editor', 'video_inst', 'record',
        )
