from django.urls import path

from .views import SongsAndMarkersListView, SongRetrieveByIdView

urlpatterns = [
    path('', SongsAndMarkersListView.as_view(), name='list_songs'),
    path('/<uuid:pk>', SongRetrieveByIdView.as_view(), name='retrieve_song'),
]
