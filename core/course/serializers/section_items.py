from rest_framework import serializers

from ...assessment.serializers import StandAloneAssessmentSerializer
from ..models import Video, Article, Source


class VideoSerializer(serializers.ModelSerializer):
    section_item_id = serializers.SerializerMethodField()
    source = serializers.CharField()

    class Meta:
        model = Video
        fields = ["section_item_id", "source", "transcript", "start_time", "end_time", "assessment"]

    def validate_source(self, value):
        """
        Ensure the provided source URL is valid and create or fetch the Source object.
        """
        source, created = Source.objects.get_or_create(url=value)
        return source

    def get_section_item_id(self, obj):
        return obj.section_item_id

class ArticleSerializer(serializers.ModelSerializer):
    section_item_id = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ["section_item_id", "content"]

    def get_section_item_id(self, obj):
        return obj.section_item_id



class SectionItemSerializer(serializers.Serializer):
    """
    Serializer for the Section model with nested items.
    """
    videos = VideoSerializer(many=True)
    articles = ArticleSerializer(many=True)
    assessments = StandAloneAssessmentSerializer(many=True)
