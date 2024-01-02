from django.contrib import admin

from .models import SongES, SongESMedia, SongESDetails


class SongESDetailsInline(admin.StackedInline):
    model = SongESDetails
    extra = 1


class SongESMediaInline(admin.StackedInline):
    model = SongESMedia
    extra = 1


@admin.register(SongES)
class SongsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'genre', 'details', 'media',)
    list_filter = ('created_at', 'updated_at')
    inlines = [SongESMediaInline, SongESDetailsInline]
    search_fields = ('title',)


@admin.register(SongESMedia)
class SongESMediaAdmin(admin.ModelAdmin):
    list_display = ('song_es', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('song_es',)


@admin.register(SongESDetails)
class SongESDetailsAdmin(admin.ModelAdmin):
    list_display = ('song_es', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('song_es',)
