# tests/models/test_course.py
import pytest
from django.test import TestCase
from ....course.models import Course, VisibilityChoices
from ..factories import CourseFactory, UserFactory

class TestCourse(TestCase):
    def setUp(self):
        self.course = CourseFactory()
        self.student = UserFactory(role='student')
        self.instructor = UserFactory(role='instructor')

    def test_course_creation(self):
        assert isinstance(self.course, Course)
        assert len(self.course.name) > 0
        assert self.course.visibility == VisibilityChoices.PUBLIC

    def test_student_access_permissions(self):
        read, write, delete = self.course.student_has_access(self.student)
        assert read is True  # Public course should be readable
        assert write is False  # Students can't write
        assert delete is False  # Students can't delete

    @pytest.mark.parametrize('visibility', [
        VisibilityChoices.PUBLIC,
        VisibilityChoices.PRIVATE,
        VisibilityChoices.UNLISTED
    ])
    def test_course_visibility_options(self, visibility):
        course = CourseFactory(visibility=visibility)
        assert course.visibility == visibility