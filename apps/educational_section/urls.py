from django.urls import path

from .views import EducationalSectionListView

urlpatterns = [
    path('', EducationalSectionListView.as_view(), name='list_sections'),
]
