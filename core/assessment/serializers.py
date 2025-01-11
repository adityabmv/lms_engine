# core/assessment/serializers.py
from drf_spectacular.utils import extend_schema_field, extend_schema_serializer
from rest_framework import serializers

from .models import (
    Question,
    NATSolution,
    DescriptiveSolution,
    MCQSolution,
    MSQSolution,
    Assessment,
    QuestionOption, QuestionType,
)



class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        exclude = ("created_at", "updated_at")


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = Question
        exclude = ("created_at", "updated_at")

    @extend_schema_field(QuestionOptionSerializer(many=True))
    def get_options(self, obj):
        if obj.type in ["MCQ", "MSQ"]:
            return QuestionOptionSerializer(obj.options, many=True).data

@extend_schema_serializer(
    examples=[
        {
            "value":1,
            "tolerance_max": 0.5,
            "tolerance_min": 0.5,
            "decimal_precision": 2,
            "solution_explaination":1,
        }
    ]
)
class NATSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NATSolution
        fields = [
            "value",
            "tolerance_max",
            "tolerance_min",
            "decimal_precision",
            "solution_explanation",
        ]


class DescriptiveSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescriptiveSolution
        fields = [
            "model_solution",
            "max_word_limit",
            "min_word_limit",
            "solution_explanation",
        ]


class MCQSolutionSerializer(serializers.ModelSerializer):
    choice = serializers.StringRelatedField()

    class Meta:
        model = MCQSolution
        fields = ["choice", "solution_explanation"]


class MSQSolutionSerializer(serializers.ModelSerializer):
    choice = serializers.StringRelatedField()

    class Meta:
        model = MSQSolution
        fields = ["choice", "solution_explanation"]


class SolutionResponseSerializer(serializers.Serializer):
    question_type = serializers.ChoiceField(choices=[qt[0] for qt in QuestionType.choices])
    solution = serializers.SerializerMethodField()

    @extend_schema_field(
        {
            "oneOf": [
                {"$ref": "#/components/schemas/NATSolution"},
                {"$ref": "#/components/schemas/DescriptiveSolution"},
                {"$ref": "#/components/schemas/MCQSolution"},
                {"$ref": "#/components/schemas/MSQSolution"},
            ]
        }
    )
    def get_solution(self, obj):
        question = obj.get('question')
        question_type = question.type

        if question_type == QuestionType.NAT:
            if hasattr(question, 'natsolution'):
                return NATSolutionSerializer(question.natsolution).data
        elif question_type == QuestionType.DESC:
            if hasattr(question, 'descriptivesolution'):
                return DescriptiveSolutionSerializer(question.descriptivesolution).data
        elif question_type == QuestionType.MCQ:
            if hasattr(question, 'mcqsolution'):
                return MCQSolutionSerializer(question.mcqsolution).data
        elif question_type == QuestionType.MSQ:
            return MSQSolutionSerializer(MSQSolution.objects.filter(question=question), many=True).data
        return None