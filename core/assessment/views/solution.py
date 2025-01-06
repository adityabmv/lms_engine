# core/assessment/views/solution.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Question
from ..serializers import (SolutionResponseSerializer)
from drf_spectacular.utils import extend_schema


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
