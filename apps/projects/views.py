from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.projects.models import Project
from apps.projects.serializers import ProjectSerializer, ProjectByIdSerializer


class ProjectListView(ListAPIView):
    """
    List of projects
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectRetrieveView(RetrieveAPIView):
    """
    Retrieve project by id
    """
    queryset = Project.objects.all()
    serializer_class = ProjectByIdSerializer
