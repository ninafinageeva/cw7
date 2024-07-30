from rest_framework import serializers

from habits.models import Habit
from habits.validators import (PeriodicityValidator, PleasantHabitValidator,
                               RewardValidator, RuntimeValidator)


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор привычки.
    """

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            RuntimeValidator(),
            PeriodicityValidator(),
            RewardValidator(),
            PleasantHabitValidator(),
        ]
        extra_kwargs = {
            "user": {"read_only": True},
            "start_at": {"format": "%H:%M"},
            "execute_at": {"format": "%d/%m/%y"},
        }
