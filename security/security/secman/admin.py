from django.contrib import admin

from django.contrib.auth.models import User




from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile
from django import forms

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
