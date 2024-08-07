from django.contrib import admin
from .models import CustomUser , Company


# class MainProfileAdmin(admin.ModelAdmin):
#     form = MainProfileForm

# admin.site.register(MainProfile, MainProfileAdmin)
admin.site.register(CustomUser)
admin.site.register(Company)
# admin.site.register(CompanyProfile)
# admin.site.register(FieldOfficer)