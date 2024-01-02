from django.urls import path

from .views import SongESListView, SongESRetrieveView

urlpatterns = [
    path('', SongESListView.as_view(), name='list_songs'),
    path('/<uuid:pk>', SongESRetrieveView.as_view(), name='retrieve_song'),
]
