from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Команда создания администратора (суперпользователя).
    """

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email="finageeva.nina@mail.ru",
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )

        user.set_password("54321")
        user.save()