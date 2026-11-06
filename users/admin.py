from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from users.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Informacion adicional', {'fields': ('telefono',)}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ('Informacion adicional', {'fields': ('telefono',)}),
    )
    list_display = ('id', 'email', 'username', 'telefono', 'is_staff', 'is_active')
