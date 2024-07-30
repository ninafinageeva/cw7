from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.servises import send_telegram_message


@shared_task
def send_habit_reminder():
    """
    Направляет напоминание о привычке в Telegram.
    """

    # Отбираем полезные привычки, срок выполнения которых наступил
    habits = Habit.objects.filter(
        start_at__lte=timezone.now().time(),
        execute_at__lte=timezone.now().date(),
        is_pleasure=False,
    )

    # Отправляем напоминания в Telegram
    for habit in habits:
        user = habit.user
        message = f"Я буду {habit.action} в {habit.start_at} {habit.place}."
        related_habit = habit.related_habit

        # Дополняем текст уведомления, если у полезной привычки есть связанная привычка или вознаграждение.

        if habit.reward:
            message += f" А сразу после этого могу {habit.reward}."
        elif related_habit:
            message += f" {related_habit}"

        if user.tg_chat_id:
            send_telegram_message(user.tg_chat_id, message)
            print(f"Напоминание отправлено пользователю {user.email}.")
        else:
            print(f"Не удалось отправить напоминание пользователю {user.email}.")

        # Обновляем дату следующего выполнения привычки
        habit.execute_at = timezone.now().date() + timedelta(days=habit.periodicity)
        habit.save()
        if related_habit:
            related_habit.execute_at = timezone.now().date() + timedelta(
                days=related_habit.periodicity
            )
            related_habit.save()
