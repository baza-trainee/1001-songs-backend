import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models

from .choices import GENRE_CYCLE_CHOICES, COUNTRY_CHOICES, REGION_CHOICES


class Song(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, unique=True)
    recording_date = models.DateField()
    performers = models.CharField(max_length=200)
    collectors = models.CharField(max_length=200)
    source = models.CharField(max_length=200)
    archive_ua = models.CharField(max_length=255)
    archive_eng = models.CharField(max_length=255)
    bibliographic_reference = models.TextField(blank=True)
    researcher_comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = "songs_db"
        ordering = ['-created_at']
        verbose_name = "Song"
        verbose_name_plural = "Songs"

    def __str__(self) -> str:
        return self.title


class SongLocation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    song = models.OneToOneField(Song, on_delete=models.CASCADE, related_name='location')
    country = models.CharField(max_length=100, default='Україна', choices=COUNTRY_CHOICES)
    region = models.CharField(max_length=100, choices=REGION_CHOICES)
    district_center = models.CharField(max_length=100)
    administrative_code = models.CharField(max_length=100)
    ethnos = models.CharField(max_length=100, default='Українці')
    ethnographic_district = models.CharField(max_length=100)
    city_ua = models.CharField(max_length=100)
    city_eng = models.CharField(max_length=100)
    unofficial_name_city = models.CharField(max_length=100, blank=True)
    recording_location = models.CharField(max_length=100, blank=True)
    coordinates = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'location'
        ordering = ['-created_at']
        verbose_name = "Song Location"
        verbose_name_plural = "Songs Locations"

    def __str__(self) -> str:
        return self.song.title


class SongDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    song = models.OneToOneField(Song, on_delete=models.CASCADE, related_name='details')
    incipit = models.CharField(max_length=100)
    genre_cycle = models.CharField(max_length=30, choices=GENRE_CYCLE_CHOICES)
    poetic_text_genre = models.CharField(max_length=50)
    texture = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'details'
        ordering = ['-created_at']
        verbose_name = "Song Details"
        verbose_name_plural = "Songs Details"

    def __str__(self) -> str:
        return self.song.title


class SongMedia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    song = models.OneToOneField(Song, on_delete=models.CASCADE, related_name='media')
    stereo_audio = models.FileField(blank=True)
    multichannel_audio = ArrayField(models.FileField(), blank=True)
    video_file = models.URLField(blank=True)
    text = models.TextField(blank=True)
    photo_of_performers = models.ImageField(blank=True)
    notes = models.CharField(max_length=255, blank=True)
    melogeographical_data = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'media'
        ordering = ['-created_at']
        verbose_name = "Song Media"
        verbose_name_plural = "Songs Media"

    def __str__(self) -> str:
        return self.song.title
