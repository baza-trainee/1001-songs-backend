from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html

from apps.songs.admin_helpers import copy_song
from apps.songs.models import Song, SongLocation, SongDetail, SongMedia


class SongLocationInline(admin.StackedInline):
    model = SongLocation
    extra = 1


class SongDetailInline(admin.StackedInline):
    model = SongDetail
    extra = 1


class SongMediaInline(admin.StackedInline):
    model = SongMedia
    extra = 1


@admin.register(Song)
class SongsAdmin(admin.ModelAdmin):
    list_display = ('copy_button', 'id', 'title', 'recording_date', 'performers',
                    'collectors', 'source', 'location', 'details', 'media',)
    list_filter = ('created_at', 'updated_at')
    inlines = [SongLocationInline, SongDetailInline, SongMediaInline]
    search_fields = ('title',)

    def get_urls(self) -> list:
        """
        Overrides URLs for the Song model in admin.
        Adds custom URL for copying songs
        """
        urls = super().get_urls()
        custom_urls = [
            path('<uuid:song_id>/copy/', self.admin_site.admin_view(copy_song), name='copy_song'),
        ]
        return custom_urls + urls

    def copy_button(self, obj: Song) -> str:
        """
        Creates a Copy button in the admin interface.
        """
        return format_html('<a class="button" href="{}">Copy</a>', reverse('admin:copy_song', args=[obj.pk]))

    copy_button.short_description = 'Copy Song'
    copy_button.allow_tags = True


@admin.register(SongLocation)
class SongLocationAdmin(admin.ModelAdmin):
    list_display = ('song', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('song',)


@admin.register(SongDetail)
class SongDetailsAdmin(admin.ModelAdmin):
    list_display = ('song', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('song',)


@admin.register(SongMedia)
class SongMediaAdmin(admin.ModelAdmin):
    list_display = ('song', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('song',)


