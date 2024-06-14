from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from auths.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = [
        "email",
        "username",
        "role",
        "is_active",
        "is_superuser",
        'id'
    ]
    search_fields = ["username", "email", "role"]
    list_filter = ["is_active", "is_superuser", "role"]
    readonly_fields = ["last_login", "date_joined"]
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("email", "role",)}),)
    fieldsets = (
        (None, {"fields": ("email", "username", "role", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")},),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")},),
        (_("Important dates"), {"fields": ("last_login", "date_joined")},),
    )
