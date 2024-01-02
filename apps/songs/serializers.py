from django.db.transaction import atomic
from rest_framework.serializers import ModelSerializer

from apps.songs.models import Song, SongLocation, SongDetail, SongMedia


class SongLocationSerializer(ModelSerializer):
    class Meta:
        model = SongLocation
        fields = ('id', 'country', 'region', 'district_center', 'administrative_code', 'ethnos',
                  'ethnographic_district', 'city_ua', 'city_eng', 'unofficial_name_city', 'recording_location',
                  'coordinates',
                  )


class SongDetailSerializer(ModelSerializer):
    class Meta:
        model = SongDetail
        fields = ('id', 'incipit', 'genre_cycle', 'poetic_text_genre', 'texture')


class SongMediaSerializer(ModelSerializer):
    class Meta:
        model = SongMedia
        fields = ('id', 'stereo_audio', 'multichannel_audio', 'video_file', 'text', 'photo_of_performers', 'notes',
                  'melogeographical_data',)


class SongSerializer(ModelSerializer):
    location = SongLocationSerializer()
    details = SongDetailSerializer()
    media = SongMediaSerializer()

    class Meta:
        model = Song
        fields = ('id', 'title', 'recording_date', 'performers', 'collectors', 'source', 'location',
                  'archive_ua', 'archive_eng', 'details', 'media',
                  )

    @atomic
    def create(self, validated_data):
        location_data = validated_data.pop('location')
        details_data = validated_data.pop('details')
        media_data = validated_data.pop('media')

        song = Song.objects.create(**validated_data)

        SongLocation.objects.create(song=song, **location_data)
        SongDetail.objects.create(song=song, **details_data)
        SongMedia.objects.create(song=song, **media_data)

        return song
