from rest_framework import viewsets
from rest_framework.exceptions import MethodNotAllowed
from drf_spectacular.utils import extend_schema, extend_schema_view
from ..models import StandAloneAssessment
from ..models.video_assessment import VideoAssessment
from ..serializers import StandAloneAssessmentSerializer, VideoAssessmentSerializer


@extend_schema_view(
    create=extend_schema(
        tags=["StandAlone Assessment"],
        summary="Create a StandAlone Assessment",
        description="Create a new standalone assessment.",
        request=StandAloneAssessmentSerializer,
        responses=StandAloneAssessmentSerializer,
    ),
    retrieve=extend_schema(
        tags=["StandAlone Assessment"],
        summary="Retrieve a StandAlone Assessment",
        description="Retrieve details of a standalone assessment by ID.",
        responses=StandAloneAssessmentSerializer,
    ),
    update=extend_schema(
        tags=["StandAlone Assessment"],
        summary="Update a StandAlone Assessment",
        description="Update an existing standalone assessment by ID.",
        request=StandAloneAssessmentSerializer,
        responses=StandAloneAssessmentSerializer,
    ),
    partial_update=extend_schema(
        tags=["StandAlone Assessment"],
        summary="Partially Update a StandAlone Assessment",
        description="Partially update fields of a standalone assessment.",
        request=StandAloneAssessmentSerializer,
        responses=StandAloneAssessmentSerializer,
    ),
    destroy=extend_schema(
        tags=["StandAlone Assessment"],
        summary="Delete a StandAlone Assessment",
        description="Delete an existing standalone assessment by ID.",
        responses={"204": "Assessment deleted successfully."},
    ),
)
class StandAloneAssessmentViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing StandAlone Assessments.
    """
    queryset = StandAloneAssessment.objects.all()
    serializer_class = StandAloneAssessmentSerializer

    def list(self, request, *args, **kwargs):
        """
        Prevent listing of all standalone assessments.
        """
        raise MethodNotAllowed("GET", detail="Listing is not allowed for this resource.")


@extend_schema_view(
    create=extend_schema(
        tags=["Video Assessment"],
        summary="Create a Video Assessment",
        description="Create a new video assessment.",
        request=VideoAssessmentSerializer,
        responses=VideoAssessmentSerializer,
    ),
    retrieve=extend_schema(
        tags=["Video Assessment"],
        summary="Retrieve a Video Assessment",
        description="Retrieve details of a video assessment by ID.",
        responses=VideoAssessmentSerializer,
    ),
    update=extend_schema(
        tags=["Video Assessment"],
        summary="Update a Video Assessment",
        description="Update an existing video assessment by ID.",
        request=VideoAssessmentSerializer,
        responses=VideoAssessmentSerializer,
    ),
    partial_update=extend_schema(
        tags=["Video Assessment"],
        summary="Partially Update a Video Assessment",
        description="Partially update fields of a video assessment.",
        request=VideoAssessmentSerializer,
        responses=VideoAssessmentSerializer,
    ),
    destroy=extend_schema(
        tags=["Video Assessment"],
        summary="Delete a Video Assessment",
        description="Delete an existing video assessment by ID.",
        responses={"204": "Assessment deleted successfully."},
    ),
)
class VideoAssessmentViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Video Assessments.
    """
    queryset = VideoAssessment.objects.all()
    serializer_class = VideoAssessmentSerializer

    def list(self, request, *args, **kwargs):
        """
        Prevent listing of all video assessments.
        """
        raise MethodNotAllowed("GET", detail="Listing is not allowed for this resource.")
