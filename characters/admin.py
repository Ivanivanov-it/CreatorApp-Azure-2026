from django.contrib import admin

from characters.models import Character


# Register your models here.

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['name','slug','title','attack','defense','hp','type','display_roles']

    def display_roles(self,obj):
        return ", ".join(role.role for role in obj.roles.all())

    display_roles.short_description = 'Roles'