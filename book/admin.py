from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from . import models

admin.site.register(models.Reservation)

class UBNumberinline(admin.StackedInline):
    model = models.UBStudent
    can_delete = False

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'ubstudent', 'is_active')
    inlines = (UBNumberinline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
