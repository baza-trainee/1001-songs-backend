import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models

from .choices_genre_songs_es import GENRE_ES_CHOICES


class SongES(models.Model):
    class Meta:
        db_table = 'songs_es'
        ordering = ['-created_at']
        verbose_name = 'Song ES'
        verbose_name_plural = 'Songs ES'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=20)
    genre = models.CharField(max_length=100, choices=GENRE_ES_CHOICES)
    text = models.TextField()
    information = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class SongESDetails(models.Model):
    class Meta:
        db_table = 'songs_es_details'
        ordering = ['-created_at']
        verbose_name = 'Song ES Details'
        verbose_name_plural = 'Songs ES Details'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    song_es = models.OneToOneField(SongES, on_delete=models.CASCADE, related_name='details')
    recording_location = models.CharField(max_length=100, blank=True)
    ethnographic_district = models.CharField(max_length=100)
    author_recording = models.CharField(max_length=100)
    performers = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.song_es.title


class SongESMedia(models.Model):
    class Meta:
        db_table = 'songs_es_media'
        ordering = ['-created_at']
        verbose_name = 'Song ES Media'
        verbose_name_plural = 'Songs ES Media'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    song_es = models.OneToOneField(SongES, on_delete=models.CASCADE, related_name='media')
    photos = ArrayField(models.ImageField(), blank=True)
    audio_example = models.FileField(blank=True)
    video_example = models.URLField(blank=True)
    ethnographic_photo = models.ImageField(blank=True)
    area = models.ImageField(blank=True)
    comment_map = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.song_es.title
