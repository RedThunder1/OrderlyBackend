from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserAccount


@admin.register(UserAccount)
class UserAccountAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("phone", "address")}),
    )
    list_display = ("username", "email", "first_name", "last_name", "phone", "is_staff")
    search_fields = ("username", "email", "phone")

