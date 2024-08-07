from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, MainProfile, FieldOfficer, CompanyProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 2:
            MainProfile.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name, email=instance.email, password=instance.password)
        elif instance.user_type == 3:
            FieldOfficer.objects.create(user=instance)
        elif instance.user_type == 4:
            CompanyProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 2:
        instance.mainprofile.save()
    elif instance.user_type == 3:
        instance.fieldofficer.save()
    elif instance.user_type == 4:
        instance.companyprofile.save()