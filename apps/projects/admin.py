from django.contrib import admin

from apps.projects.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
            'title', 'date_event', 'brief_description', 'location', 'photo_1', 'text_1_intro',
            'photo_2', 'text_2', 'author', 'editor', 'svitliny',
    )
    list_filter = ('created_at', 'updated_at',)
    search_fields = ('title',)
