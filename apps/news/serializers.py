from rest_framework.serializers import ModelSerializer
from apps.news.models import News, NewsDetail


class NewsSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"


class NewsDetailsSerializer(ModelSerializer):
    class Meta:
        model = NewsDetail
        fields = "__all__"
