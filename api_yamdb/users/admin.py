from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'is_staff',
    )
    list_editable = ('role',)
    search_fields = ('username', 'email', 'first_name', 'last_name',)
    fieldsets = BaseUserAdmin.fieldsets
    empty_value_display = 'Не задано'
