# tests/views/test_course_views.py
from rest_framework.test import APITestCase
from rest_framework import status
from ..factories import CourseFactory, UserFactory

class TestCourseViewSet(APITestCase):
    def setUp(self):
        self.user = UserFactory(role='instructor')
        self.client.force_authenticate(user=self.user)
        self.course = CourseFactory()
        self.list_url = '/api/courses/'
        self.detail_url = f'/api/courses/{self.course.id}/'

    def test_list_courses(self):
        response = self.client.get(self.list_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_create_course(self):
        data = {
            'name': 'New Course',
            'description': 'Course Description',
            'visibility': 'public'
        }
        response = self.client.post(self.list_url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == data['name']