from django.urls import path

from habits.apps import HabitsConfig
from habits.views import (HabitCreateAPIView, HabitDestroyAPIView,
                          HabitListAPIView, HabitRetrieveAPIView,
                          HabitUpdateAPIView, PublicHabitListAPIView)

app_name = HabitsConfig.name

urlpatterns = [
    path("public/", PublicHabitListAPIView.as_view(), name="public-habits"),
    path("create/", HabitCreateAPIView.as_view(), name="habit-create"),
    path("", HabitListAPIView.as_view(), name="habits"),
    path("<int:pk>/", HabitRetrieveAPIView.as_view(), name="habit"),
    path("<int:pk>/update/", HabitUpdateAPIView.as_view(), name="habit-update"),
    path("<int:pk>/delete/", HabitDestroyAPIView.as_view(), name="habit-delete"),
]
