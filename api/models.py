from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=244, null=True)
    gio_location = models.JSONField(null=True)
    has_holiday = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    def __str__(self):
        return self.content[:50]  # Return the first 50 characters of the content

from django.db.models.signals import post_save
from .utils import get_geolocation_data, check_holiday
from django.dispatch import receiver

# @receiver(post_save, sender=User)
# def enrich_user(sender, instance, created, **kwargs):
#     if created:
#         ip_address = instance.last_login_ip  # Assuming you have a field to store the last login IP address in your User model
#         geolocation_data = get_geolocation_data(ip_address)
#         if geolocation_data:
#             instance.location = geolocation_data.get("country", "")
#             instance.save()

#         signup_date = instance.date_joined.date()
#         country_code = instance.location  # Assuming the location field is already populated with the country code
#         holiday_data = check_holiday(signup_date, country_code)
#         if holiday_data:
#             instance.has_holiday = True  # Assuming you have a BooleanField 'has_holiday' to store the holiday information in your User model
#             instance.save()
