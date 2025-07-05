from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.models import User
from materials.models import Course, Lesson, Subscription


class CourseLessonSubscriptionTests(APITestCase):

    def setUp(self):
        # Создаём пользователей
        self.user = User.objects.create(email="testuser@mail.com")
        self.user.set_password("12345")
        self.user.save()

        self.other_user = User.objects.create(email="other@mail.com")
        self.other_user.set_password("12345")
        self.other_user.save()

        # Создаём курс
        self.course = Course.objects.create(
            title="Тестовый курс", description="Описание курса", owner=self.user
        )

        # Создаём урок
        self.lesson = Lesson.objects.create(
            title="Тестовый урок",
            description="Описание урока",
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            owner=self.user,
            course=self.course,
        )

        # Подписка
        self.subscription = Subscription.objects.create(
            user=self.user, course=self.course
        )

        # Авторизуемся
        self.client.force_authenticate(user=self.user)

    def test_get_course_list(self):
        url = reverse("course-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_course(self):
        url = reverse("course-list")
        data = {"title": "Новый курс", "description": "Описание нового курса"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_course(self):
        url = reverse("course-detail", args=[self.course.id])
        data = {"title": "Обновлённый курс", "description": "Новое описание"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_course(self):
        url = reverse("course-detail", args=[self.course.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_subscription(self):
        url = reverse("subscription-create")
        data = {"course": self.course.id}
        response = self.client.post(url, data)
        self.assertIn(
            response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED]
        )

    def test_delete_subscription(self):
        url = reverse("subscription-delete", args=[self.subscription.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
