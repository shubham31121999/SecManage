from django.contrib import admin
from .models import CustomUser, MainProfile, CompanyProfile, FieldOfficer
from .forms import MainProfileForm

class MainProfileAdmin(admin.ModelAdmin):
    form = MainProfileForm

admin.site.register(MainProfile, MainProfileAdmin)
admin.site.register(CustomUser)
admin.site.register(CompanyProfile)
admin.site.register(FieldOfficer)