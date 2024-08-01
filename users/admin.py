from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "email",
        "phone",
        "tg_chat_id",
        "is_staff",
        "is_superuser",
    )
