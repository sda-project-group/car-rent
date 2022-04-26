from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from carrent.carrentapp.models import UserCustom
from carrent.carrentapp.forms import UserCreationForm,UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'username', 'is_admin', 'is_staff')
    list_filter = ('is_admin', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'username')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'birthdate', 'addr_city', 'addr_street', 'addr_post_code', 'mobile_nr',)}),
        ('Permissions', {'fields': ('is_admin','is_staff',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'birthdate', 'addr_city', 'addr_street', 'addr_post_code', 'mobile_nr'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Register your models here.
admin.site.register(UserCustom, UserAdmin)
admin.site.unregister(Group)
