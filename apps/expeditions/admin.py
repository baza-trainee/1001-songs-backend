from django.contrib import admin

from apps.expeditions.models import Expedition


@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = (
            'title', 'date_event', 'brief_description', 'location', 'type_expedition', 'coordinates',
            'text_1', 'video_1', 'text_2', 'text_3', 'text_4', 'text_5', 'photo', 'comment_to_photo', 'text_6',
            'video_2', 'comment_to_video_2', 'text_7', 'video_3', 'comment_to_video_3', 'text_8', 'video_4',
            'comment_to_video_4', 'text_9', 'text_10', 'collectors', 'editor', 'video_inst', 'record',
    )
    list_filter = ('created_at', 'updated_at',)
    search_fields = ('title',)
