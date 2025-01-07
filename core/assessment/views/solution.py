# core/assessment/views/solution.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from ..models import Question, NATSolution, DescriptiveSolution, MCQSolution, MSQSolution
from ..serializers import (SolutionResponseSerializer)
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Question
from ..serializers import (
    SolutionResponseSerializer,
    NATSolutionSerializer,
    DescriptiveSolutionSerializer,
    MCQSolutionSerializer,
    MSQSolutionSerializer
)


@extend_schema(
    tags=["Solution"],
    operation_id="get_solution_by_question",
    description="Retrieve the solution for a specific question by its ID.",
    responses={
        200: SolutionResponseSerializer,
        404: {"description": "Question not found or solution not available."},
    },
    summary="Get Solution by Question",
)
@api_view(["GET"])
def get_solution_by_question(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = SolutionResponseSerializer({
        "question": question,
        "question_type": question.type,
    })

    solution_data = serializer.data.get('solution')

    if not solution_data:
        return Response({"error": "Solution not found for the given question"}, status=status.HTTP_404_NOT_FOUND)

    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    create=extend_schema(
        tags=["Solution"],
        summary="Create a Solution",
        description="Create a new question for an assessment.",
        request=SolutionResponseSerializer,
        responses=SolutionResponseSerializer,
    ),
    update=extend_schema(
        tags=["Solution"],
        summary="Update a Solution",
        description="Update an existing question by ID.",
        request=SolutionResponseSerializer,
        responses=SolutionResponseSerializer,
    ),
    partial_update=extend_schema(
        tags=["Solution"],
        summary="Partially Update a Solution",
        description="Update selected fields of an existing question.",
        request=SolutionResponseSerializer,
        responses=SolutionResponseSerializer,
    ),
    destroy=extend_schema(
        tags=["Solution"],
        summary="Delete a Solution",
        description="Delete an existing solution by ID.",
        responses={"204": "Solution deleted successfully."},
    ),
)
class SolutionViewSet(viewsets.ModelViewSet):
    serializer_class = SolutionResponseSerializer

    def get_queryset(self):
        """
        Combine querysets from all concrete solution models.
        """
        return NATSolution.objects.all() | \
               DescriptiveSolution.objects.all() | \
               MCQSolution.objects.all() | \
               MSQSolution.objects.all()


    def list(self, request, *args, **kwargs):
        """
        Disable the list (GET /solutions/) endpoint.
        """
        return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        """
        Disable the retrieve (GET /solutions/{id}/) endpoint.
        """
        return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
