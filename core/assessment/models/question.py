# core/assessment/models/question.py

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from ...auth.permissions import ModelPermissionsMixin
from ...utils.models import TimestampMixin
from .. import constants as ct


class QuestionType(models.TextChoices):
    MCQ = "MCQ", "Multiple Choice Question"
    MSQ = "MSQ", "Multiple Select Question"
    NAT = "NAT", "Numerical Answer Type"
    DESC = "DESC", "Descriptive Question"


class Question(TimestampMixin, ModelPermissionsMixin, models.Model):
    assessment = models.ForeignKey(
        "assessment.StandAloneAssessment", on_delete=models.CASCADE, related_name="questions", null=True, blank=True)
    video_assessment = models.ForeignKey(
        "assessment.VideoAssessment", on_delete=models.CASCADE, related_name="questions", null=True, blank=True
    )
    text = models.TextField(max_length=ct.QUESTION_TEXT_MAX_LEN, help_text="The question text.")
    hint = models.TextField(null=True, blank=True, max_length=ct.QUESTION_HINT_MAX_LEN, help_text="A hint to help the student.")
    type = models.CharField(choices=QuestionType.choices, max_length=10, help_text="The type of question.")
    partial_marking = models.BooleanField(default=False, null=True, help_text="Enable partial marking for the question.")
    marks = models.IntegerField(
        validators=[
            MinValueValidator(ct.QUESTION_MARKS_MIN_VAL),
            MaxValueValidator(ct.QUESTION_MARKS_MAX_VAL),
        ]
        ,
        help_text="The maximum marks for the question."
    )

    def __getattr__(self, name):
        """
        Delegate permission checks to the related assessment object.
        """
        if name.endswith("_has_access"):
            return getattr(self.assessment, name)
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'"
        )

    def admin_has_access(self, user: "User"):
        return True, True, True