from rest_framework import serializers

from ...assessment.serializers import AssessmentSerializer
from ..models import Video, Article, Source


class VideoSerializer(serializers.ModelSerializer):
    source = serializers.CharField()

    class Meta:
        model = Video
        exclude = ['created_at', 'updated_at']

    def validate_source(self, value):
        """
        Ensure the provided source URL is valid and create or fetch the Source object.
        """
        source, created = Source.objects.get_or_create(url=value)
        return source

class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        exclude = ['created_at', 'updated_at']


class SectionItemSerializer(serializers.Serializer):
    """
    Serializer for the Section model with nested items.
    """
    videos = VideoSerializer(many=True)
    articles = ArticleSerializer(many=True)
    assessments = AssessmentSerializer(many=True)
