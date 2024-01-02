from django.urls import path

from .views import ExpeditionListView, ExpeditionRetrieveView

urlpatterns = [
    path('', ExpeditionListView.as_view(), name='list_expeditions'),
    path('/<int:pk>', ExpeditionRetrieveView.as_view(), name='retrieve_expedition'),
]
