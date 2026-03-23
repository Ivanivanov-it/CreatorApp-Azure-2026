from django.contrib import admin

from common.models import Role


# Register your models here.

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['role']