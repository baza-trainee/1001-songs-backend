from django.db.transaction import atomic
from rest_framework.serializers import ModelSerializer

from .models import SongES, SongESMedia, SongESDetails


class SongESMediaSerializer(ModelSerializer):
    class Meta:
        model = SongESMedia
        fields = ('id', 'photos', 'audio_example', 'video_example', 'ethnographic_photo', 'area', 'comment_map')


class SongESDetailsSerializer(ModelSerializer):
    class Meta:
        model = SongESDetails
        fields = ('id', 'recording_location', 'ethnographic_district', 'author_recording', 'performers')


class SongESSerializer(ModelSerializer):
    details = SongESDetailsSerializer()
    media = SongESMediaSerializer()

    class Meta:
        model = SongES
        fields = ('id', 'title', 'genre', 'text', 'information', 'details', 'media',)

    @atomic
    def create(self, validated_data):
        details_data = validated_data.pop('details')
        media_data = validated_data.pop('media')

        song_es = SongES.objects.create(**validated_data)

        SongESDetails.objects.create(song_es=song_es, **details_data)
        SongESMedia.objects.create(song_es=song_es, **media_data)

        return song_es
