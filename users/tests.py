from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(email="user1@example.com")

    def test_str_user(self):
        """
        Тестирование отображения имени пользователя
        """
        self.assertEqual(str(self.user1), self.user1.email)

    def test_user_create(self):
        """
        Тестирование создания нового пользователя
        """
        url = reverse("users:register")
        data = {
            "email": "user2@example.com",
            "password": "test123",
            "tg_chat_id": "123123123",
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email="user2@example.com")
        self.assertEqual(user.tg_chat_id, data["tg_chat_id"])
        self.assertTrue(user.check_password("test123"))
