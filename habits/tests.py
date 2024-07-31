from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(email="user1@example.com")
        self.user2 = User.objects.create(email="user2@example.com")
        self.user3 = User.objects.create(
            email="user3@example.com", is_staff=True, is_superuser=True
        )
        self.good_habit1 = Habit.objects.create(
            place="здесь",
            start_at=timezone.now().time(),
            action="проводить тестирование своей привычки",
            user=self.user1,
            runtime=timedelta(minutes=1),
        )
        self.good_habit2 = Habit.objects.create(
            place="здесь",
            start_at=timezone.now().time(),
            action="проводить тестирование чужой привычки",
            user=self.user2,
            runtime=timedelta(minutes=1),
        )
        self.pleasant_habit1 = Habit.objects.create(
            place="здесь",
            start_at=timezone.now().time(),
            action="улыбаться",
            user=self.user1,
            runtime=timedelta(minutes=1),
            is_pleasure=True,
            is_public=True,
        )
        self.pleasant_habit2 = Habit.objects.create(
            place="здесь",
            start_at=timezone.now().time(),
            action="визуализировать свое желание",
            user=self.user2,
            runtime=timedelta(minutes=1),
            is_pleasure=True,
            is_public=True,
        )
        self.good_habit3 = Habit.objects.create(
            place="здесь",
            start_at=timezone.now().time(),
            action="проводить тестирование чужой привычки",
            user=self.user2,
            runtime=timedelta(minutes=1),
            is_public=True,
        )
        self.client.force_authenticate(user=self.user1)

    def test_str_habit(self):
        """
        Тестирование строчного представления привычки
        """
        habit = Habit.objects.get(pk=self.good_habit1.pk)
        self.assertEqual(
            str(habit), f"Я буду {habit.action} в {habit.start_at} {habit.place}."
        )

    def test_owner_habit_retrieve(self):
        """
        Тестирование просмотра привычки ее владельцем
        """
        url = reverse("habits:habit", args=(self.good_habit1.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.good_habit1.action)

    def test_other_user_habit_retrieve(self):
        """
        Тестирование просмотра чужой привычки пользователем
        """
        url = reverse("habits:habit", args=(self.good_habit2.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_habit_create(self):
        """
        Тестирование создания привычки
        """
        url = reverse("habits:habit-create")
        data = [
            {
                "place": "здесь",
                "start_at": "18:00",
                "action": "тестировать корректное создание привычки",
                "runtime": "00:01:00",
                "user": self.user1.pk,
                "related_habit": self.pleasant_habit1.pk,
            },
            {
                "place": "здесь",
                "start_at": "18:00",
                "action": "тестировать корректность времени выполнения при создании привычки",
                "runtime": "00:03:00",
                "user": self.user1.pk,
            },
            {
                "place": "здесь",
                "start_at": "18:00",
                "action": "тестировать корректное создание привычки",
                "runtime": "00:01:00",
                "user": self.user1.pk,
                "related_habit": self.pleasant_habit1.pk,
                "periodicity": 8,
            },
            {
                "place": "здесь",
                "start_at": "18:00",
                "action": "тестировать корректное создание привычки",
                "runtime": "00:01:00",
                "user": self.user1.pk,
                "related_habit": self.pleasant_habit1.pk,
                "reward": "выпить кофе",
            },
            {
                "place": "здесь",
                "start_at": "18:00",
                "action": "тестировать корректное создание привычки",
                "runtime": "00:01:00",
                "user": self.user1.pk,
                "related_habit": self.good_habit1.pk,
            },
            {
                "place": "здесь",
                "start_at": "18:00",
                "action": "тестировать корректное создание привычки",
                "runtime": "00:01:00",
                "user": self.user1.pk,
                "related_habit": self.pleasant_habit1.pk,
                "is_pleasure": True,
            },
            {
                "place": "здесь",
                "start_at": "18:00",
                "action": "тестировать корректное создание привычки",
                "runtime": "00:01:00",
                "user": self.user1.pk,
                "reward": "выпить кофе",
                "is_pleasure": True,
            },
        ]

        # Тестируем корректное создание привычки
        response = self.client.post(url, data=data[0])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Habit.objects.get(action="тестировать корректное создание привычки")
        )
        self.assertFalse(
            Habit.objects.get(
                action="тестировать корректное создание привычки"
            ).is_pleasure
        )
        self.assertFalse(
            Habit.objects.get(
                action="тестировать корректное создание привычки"
            ).is_public
        )

        # Тестируем создание привычки с некорректным временем выполнения
        response = self.client.post(url, data=data[1])
        message = response.json()["non_field_errors"]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            message, ["Время на выполнение должно быть не более 120 секунд."]
        )

        # Тестируем создание привычки с некорректной периодичностью
        response = self.client.post(url, data=data[2])
        message = response.json()["non_field_errors"]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            message,
            ["Промежуток между выполнениями привычки не может превышать 7 дней."],
        )

        # Тестируем создание привычки с одновременным использованием вознаграждения и связанной приятной привычки
        response = self.client.post(url, data=data[3])
        message = response.json()["non_field_errors"]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            message,
            ["Нельзя указывать вознаграждение и связанную привычку одновременно."],
        )

        # Тестируем создание привычки со связанной полезной привычкой
        response = self.client.post(url, data=data[4])
        message = response.json()["non_field_errors"]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(message, ["Связанная привычка должна быть приятной."])

        # Тестируем создание приятной привычки со связанной привычкой
        response = self.client.post(url, data=data[5])
        message = response.json()["non_field_errors"]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            message,
            [
                "У приятной привычки не может быть связанной привычки или вознаграждения."
            ],
        )

        # Тестируем создание приятной привычки с вознаграждением
        response = self.client.post(url, data=data[6])
        message = response.json()["non_field_errors"]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            message,
            [
                "У приятной привычки не может быть связанной привычки или вознаграждения."
            ],
        )

    def test_owner_habit_update(self):
        """
        Тестирование редактирования привычки владельцем
        """
        url = reverse("habits:habit-update", args=(self.good_habit1.pk,))
        data = {
            "action": "тестировать редактирование привычки владельцем",
        }

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit = Habit.objects.get(pk=self.good_habit1.pk)
        self.assertEqual(habit.action, data["action"])

    def test_other_user_habit_update(self):
        """
        Тестирование редактирования чужой привычки пользователем
        """
        url = reverse("habits:habit-update", args=(self.good_habit2.pk,))
        data = {
            "action": "тестировать редактирование чужой привычки пользователем",
        }

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        habit = Habit.objects.get(pk=self.good_habit2.pk)
        self.assertNotEqual(habit.action, data["action"])

    def test_owner_habit_delete(self):
        """
        Тестирование удаления привычки владельцем
        """
        url = reverse("habits:habit-delete", args=(self.good_habit1.pk,))

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(pk=self.good_habit1.pk).exists())

    def test_other_user_habit_delete(self):
        """
        Тестирование удаления чужой привычки пользователем
        """
        url = reverse("habits:habit-delete", args=(self.good_habit2.pk,))

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Habit.objects.filter(pk=self.good_habit2.pk).exists())

    def test_habit_list(self):
        """
        Тестирование получения списка привычек владельцем
        """
        url = reverse("habits:habits")

        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data["results"]), 2)

    def test_public_habit_list(self):
        """
        Тестирование получения списка публичных привычек
        """
        url = reverse("habits:public-habits")

        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data["results"]), 3)

    def test_superuser_habit_list(self):
        """
        Тестирование получения списка привычек суперпользователем
        """
        self.client.force_authenticate(user=self.user3)

        url = reverse("habits:habits")

        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data["results"]), 5)
