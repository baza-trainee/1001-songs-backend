

from django.urls import path

from .views import NewsDetailView, NewsListDetailView, NewsView, NewsViewAll

urlpatterns = [
    path('', NewsViewAll.as_view(), name='list_create_news'),
    path('/<int:pk>', NewsView.as_view(), name='list_create_news'),
    path('/detail', NewsListDetailView.as_view(), name='news_list_create_view'),
    path('/detail/<int:pk>', NewsDetailView.as_view(), name='news_retrieve_view')
]

