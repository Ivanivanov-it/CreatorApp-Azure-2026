from django.contrib import admin

from partners.models import Partner


# Register your models here.

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name','slug','title','attack','defense','hp','display_character','display_roles']


    def display_character(self,obj):
        return obj.character.name

    def display_roles(self,obj):
        return ", ".join(role.role for role in obj.roles.all())

    display_roles.short_description = 'Roles'
    display_character.short_description = 'Related Character'
