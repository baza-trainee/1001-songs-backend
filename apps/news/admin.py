from django.contrib import admin

from apps.news.models import News, NewsDetail


class NewsDetailInline(admin.StackedInline):
    model = NewsDetail
    extra = 1


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsDetailInline]
    list_display = ('type_of_news', 'date', 'news_title', 'location')
    list_filter = ('type_of_news', 'date')
    search_fields = ('news_title', 'location')
    ordering = ('date',)


@admin.register(NewsDetail)
class NewsDetailAdmin(admin.ModelAdmin):
    list_display = ('news_title', 'date', 'location', 'author', 'editor')
    list_filter = ('date',)
    search_fields = ('news_title', 'location')
    ordering = ('date',)
