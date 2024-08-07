from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 1)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('user_type') != 1:
            raise ValueError('Superuser must have user_type=1.')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'superuser'),
        (2, 'Main'),
        (3, 'field_officer'),
        (4, 'company'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)
    user_id = models.CharField(max_length=20,unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    objects = CustomUserManager()
    
    
# class Company(AbstractUser):
    
#     user_type = models.OneToOneField(choices=CustomUser.USER_TYPE_CHOICES, on_delete=models.CASCADE)
#     user_id = models.CharField(max_length=20,unique=True)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128)

#     def __str__(self):
#         return f'{self.first_name} {self.last_name}'

#     objects = CustomUserManager()

# class MainProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     email = models.EmailField()
#     password = models.CharField(max_length=128)

#     def __str__(self):
#         return f'{self.first_name} {self.last_name}'

# class CompanyProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 4})
#     name = models.CharField(max_length=255)
#     address = models.TextField()
#     logo = models.ImageField(upload_to='company_logos/')

#     def __str__(self):
#         return self.name

# class FieldOfficer(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 3})
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     email = models.EmailField()
#     age = models.IntegerField()
#     gender = models.CharField(max_length=10)

#     def __str__(self):
#         return f'{self.first_name} {self.last_name}'