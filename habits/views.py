from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated

from habits.models import Habit
from habits.paginators import CustomPagination
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer


class HabitCreateAPIView(CreateAPIView):
    """
    Контроллер создания новой привычки.
    """

    serializer_class = HabitSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwner,
    )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitListAPIView(ListAPIView):
    """
    Контроллер получения списка привычек пользователя.
    """

    serializer_class = HabitSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwner,
    )
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        if not user.is_superuser:
            return Habit.objects.filter(user=user)
        return Habit.objects.all()


class HabitRetrieveAPIView(RetrieveAPIView):
    """
    Контроллер получения информации о привычке.
    """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwner,
    )


class HabitUpdateAPIView(UpdateAPIView):
    """
    Контроллер изменения информации о привычке.
    """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwner,
    )


class HabitDestroyAPIView(DestroyAPIView):
    """
    Контроллер удаления привычки.
    """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwner,
    )


class PublicHabitListAPIView(ListAPIView):
    """
    Контроллер получения списка публичных привычек.
    """

    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    permission_classes = (AllowAny,)
    pagination_class = CustomPagination
