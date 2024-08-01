from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "action",
        "start_at",
        "execute_at",
        "periodicity",
        "is_public",
        "is_pleasure",
    )

