# tests/permissions/test_course_permissions.py
import pytest
from django.test import TestCase
from ..factories import CourseFactory, UserFactory

class TestCoursePermissions(TestCase):
    @pytest.mark.parametrize('role,expected_access', [
        ('student', (True, False, False)),
        ('instructor', (True, True, False)),
        ('admin', (True, True, True))
    ])
    def test_role_based_permissions(self, role, expected_access):
        user = UserFactory(role=role)
        course = CourseFactory()
        access = course.admin_has_access(user)
        assert access == expected_access