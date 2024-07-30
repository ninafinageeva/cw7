from django.db import models

from users.models import NULLABLE


class Habit(models.Model):
    """
    Модель привычки.
    """

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name="Создатель привычки"
    )
    place = models.CharField(max_length=250, verbose_name="Место выполнения")
    start_at = models.TimeField(verbose_name="Время начала выполнения")
    action = models.CharField(max_length=250, verbose_name="Действие")
    periodicity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Периодичность выполнения",
        help_text="Промежуток между выполнениями привычки в днях.",
    )
    is_pleasure = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки"
    )
    related_habit = models.ForeignKey(
        "self", **NULLABLE, on_delete=models.SET_NULL, verbose_name="Связанная привычка"
    )
    reward = models.CharField(max_length=250, **NULLABLE, verbose_name="Вознаграждение")
    runtime = models.DurationField(verbose_name="Время на выполнение")
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")
    execute_at = models.DateField(auto_now_add=True, verbose_name="Дата выполнения")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f"Я буду {self.action} в {self.start_at} {self.place}."
    
