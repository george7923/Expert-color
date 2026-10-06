from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Rol, Utilizator


@admin.register(Utilizator)
class UtilizatorAdmin(UserAdmin):
    list_display = ("username", "email", "rol", "is_active")
    fieldsets = UserAdmin.fieldsets + (("Rol", {"fields": ("rol",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Rol", {"fields": ("rol",)}),)


admin.site.register(Rol)
