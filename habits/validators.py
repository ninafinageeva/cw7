from datetime import timedelta

from rest_framework.serializers import ValidationError


class RuntimeValidator:
    """
    Валидатор времени выполнения привычки.
    """

    def __call__(self, attrs):
        runtime = attrs.get("runtime")
        if runtime and runtime > timedelta(minutes=2):
            raise ValidationError(
                "Время на выполнение должно быть не более 120 секунд."
            )


class PeriodicityValidator:
    """
    Валидатор периодичности выполнения привычки.
    """

    def __call__(self, attrs):
        periodicity = attrs.get("periodicity")
        if periodicity and periodicity > 7:
            raise ValidationError(
                "Промежуток между выполнениями привычки не может превышать 7 дней."
            )


class RewardValidator:
    """
    Валидатор вознаграждения полезной привычки.
    """

    def __call__(self, attrs):
        related_habit = attrs.get("related_habit")
        if related_habit and attrs.get("reward"):
            raise ValidationError(
                "Нельзя указывать вознаграждение и связанную привычку одновременно."
            )
        if related_habit and not related_habit.is_pleasure:
            raise ValidationError("Связанная привычка должна быть приятной.")


class PleasantHabitValidator:
    """
    Валидатор приятной привычки.
    """

    def __call__(self, attrs):
        is_pleasure = attrs.get("is_pleasure")
        if is_pleasure and (attrs.get("related_habit") or attrs.get("reward")):
            raise ValidationError(
                "У приятной привычки не может быть связанной привычки или вознаграждения."
            )
