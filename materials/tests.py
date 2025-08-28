from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class LessonSubscriptionTestCase(APITestCase):

    def setUp(self):
        """Создаёт тестового пользователя, курс и урок.
        Выполняет аутентификацию клиента от имени пользователя при помощи force_authenticate"""

        self.user = User.objects.create(email="1@1.ru")
        self.course = Course.objects.create(title="Test Course", owner=self.user)
        self.lesson = Lesson.objects.create(title="Test Lesson", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_user_subscribe(self):
        """Проверяет подписку пользователя на курс через API"""

        url = reverse('users:subscription')  # пример namespace 'users' и имя маршрута 'subscription'
        data = {'course_id': self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_list_lessons(self):
        """Проверяет получение списка уроков"""

        url = reverse('materials:lesson_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.lesson.id,
                    'title': self.lesson.title,
                    'description': self.lesson.description,
                    'course': self.course.id,
                    'link_to_video': None
                }
            ]
        }
        self.assertEqual(response.data, expected)

    def test_retrieve_lesson(self):
        """Проверяет получение данных конкретного урока"""

        url = reverse('materials:lesson_get', args=[self.lesson.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected = {
            'id': self.lesson.id,
            'title': self.lesson.title,
            'description': self.lesson.description,
            'course': self.course.id,
            'link_to_video': None
        }
        self.assertEqual(response.data, expected)

    def test_create_lesson_invalid_url(self):
        """Проверяет создание урока с некорректной ссылкой на видео"""

        url = reverse('materials:lesson_create')
        data = {
            "title": "test2",
            "course": self.course.id,
            "link_to_video": "www.fsfsf.com"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'link_to_video': ["Ссылка должна вести на ресурсы: 'youtube.com'"]})

    def test_create_lesson_valid_url(self):
        """Проверяет успешное создание урока с правильной ссылкой на видео"""

        url = reverse('materials:lesson_create')
        data = {
            "title": "test2",
            "course": self.course.id,
            "link_to_video": "https://www.youtube.com"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.created_lesson_id = response.json().get('id')

    def test_update_lesson(self):
        """Проверяет обновление существующего урока"""
        self.test_create_lesson_valid_url()  # создаём урок, чтобы обновить
        url = reverse('materials:lesson_update', args=[self.created_lesson_id])
        data = {
            "title": "test_test",
            "link_to_video": "www.youtube.com"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], "test_test")

    def test_delete_lesson(self):
        """Проверяет удаление урока"""

        self.test_create_lesson_valid_url()  # создаём урок, чтобы удалить
        url = reverse('materials:lesson_delete', args=[self.created_lesson_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        list_url = reverse('materials:lesson_list')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("count"), 1)
