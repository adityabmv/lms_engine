from rest_framework import generics, viewsets
from rest_framework.exceptions import NotFound, MethodNotAllowed
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from ..models import Section, Video, Article
from ..serializers import SectionItemSerializer, VideoSerializer, ArticleSerializer


@extend_schema(
tags=["Item"],
        summary="List Section Items",
        description="Retrieve a list of section items filtered by course, module, or section ID.",
        parameters=[
            OpenApiParameter(
                name="course_id",
                description="Filter items by course ID",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="module_id",
                description="Filter items by module ID",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="section_id",
                description="Filter items by section ID",
                required=False,
                type=int,
            ),
        ],
        responses=SectionItemSerializer,
)
class SectionItemListView(generics.ListAPIView):
    serializer_class = SectionItemSerializer

    def get_queryset(self):
        course_id = self.request.query_params.get('course_id')
        module_id = self.request.query_params.get('module_id')
        section_id = self.request.query_params.get('section_id')

        if course_id is not None:
            return Section.objects.filter(module__course__id=course_id)

        if module_id is not None:
            return Section.objects.filter(module__id=module_id)

        if section_id is not None:
            return Section.objects.filter(id=section_id)

        raise NotFound("You must specify one of 'course_id', 'module_id', or 'section_id'.")


@extend_schema_view(
    create=extend_schema(
        tags=["Video"],
        summary="Create a Video",
        description="Create a new video resource.",
        request=VideoSerializer,
        responses=VideoSerializer,
    ),
    retrieve=extend_schema(
        tags=["Video"],
        summary="Retrieve a Video",
        description="Get details of a specific video.",
        responses=VideoSerializer,
    ),
    update=extend_schema(
        tags=["Video"],
        summary="Update a Video",
        description="Update an existing video with new data.",
        request=VideoSerializer,
        responses=VideoSerializer,
    ),
    partial_update=extend_schema(
        tags=["Video"],
        summary="Partially Update a Video",
        description="Update selected fields of an existing video.",
        request=VideoSerializer,
        responses=VideoSerializer,
    ),
    destroy=extend_schema(
        tags=["Video"],
        summary="Delete a Video",
        description="Delete an existing video.",
        responses={"204": "Video deleted successfully."},
    ),
)
class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed("GET", detail="Listing is not allowed for this resource.")


@extend_schema_view(
    create=extend_schema(
        tags=["Article"],
        summary="Create an Article",
        description="Create a new article resource.",
        request=ArticleSerializer,
        responses=ArticleSerializer,
    ),
    retrieve=extend_schema(
        tags=["Article"],
        summary="Retrieve an Article",
        description="Get details of a specific article.",
        responses=ArticleSerializer,
    ),
    update=extend_schema(
        tags=["Article"],
        summary="Update an Article",
        description="Update an existing article with new data.",
        request=ArticleSerializer,
        responses=ArticleSerializer,
    ),
    partial_update=extend_schema(
        tags=["Article"],
        summary="Partially Update an Article",
        description="Update selected fields of an existing article.",
        request=ArticleSerializer,
        responses=ArticleSerializer,
    ),
    destroy=extend_schema(
        tags=["Article"],
        summary="Delete an Article",
        description="Delete an existing article.",
        responses={"204": "Article deleted successfully."},
    ),
)
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed("GET", detail="Listing is not allowed for this resource.")