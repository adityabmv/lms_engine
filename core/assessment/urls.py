from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import QuestionViewSet, get_solution_by_question
from .views.assessment import StandAloneAssessmentViewSet, VideoAssessmentViewSet

router = DefaultRouter()
router.register(r'video-assessments', VideoAssessmentViewSet, basename='video-assessment')
router.register(r'questions', QuestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('solutions/<int:question_id>/', get_solution_by_question, name='get_solution_by_question'),
]
