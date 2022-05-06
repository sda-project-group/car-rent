from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

from .forms import UserCreationForm,UserChangeForm
from . models import Car, CarModel, CarBrand, BasePrice, Order


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
admin.site.register(get_user_model(), UserAdmin)
admin.site.unregister(Group)
admin.site.register(Car)
admin.site.register(CarModel)
admin.site.register(CarBrand)
admin.site.register(BasePrice)
admin.site.register(Order)
