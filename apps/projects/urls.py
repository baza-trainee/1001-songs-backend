from django.urls import path

from .views import ProjectListView, ProjectRetrieveView

urlpatterns = [
    path('', ProjectListView.as_view(), name='list_projects'),
    path('/<int:pk>', ProjectRetrieveView.as_view(), name='retrieve_project'),
]
