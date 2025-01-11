# tests/serializers/test_course_serializers.py
from django.test import TestCase
from core.course.serializers import CourseDetailSerializer
from core.course.tests.factories import CourseFactory

class TestCourseSerializer(TestCase):
    def setUp(self):
        self.course = CourseFactory()
        self.serializer = CourseDetailSerializer(instance=self.course)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        expected_fields = {
            'course_id', 'name', 'description',
            'visibility', 'module_count'
        }
        assert set(data.keys()) >= expected_fields

    def test_module_count_value(self):
        assert isinstance(self.serializer.data['module_count'], int)