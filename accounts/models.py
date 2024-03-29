import uuid
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta


class PersonManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):

        if email is not None:
            unverified_email = self.normalize_email(email)
        else:
            unverified_email = None

        if extra_fields.get('is_superuser') is True:
            user = self.model(
                username=email,
                email=email,
                is_verified=True,
                **extra_fields
            )
        else:
            uid = f'{uuid.uuid4()}@hydroserver-temp.org'
            user = self.model(
                username=uid,
                email=uid,
                unverified_email=unverified_email,
                **extra_fields
            )

        if password is not None:
            user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class Organization(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    code = models.CharField(max_length=200)
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=255)
    link = models.URLField(max_length=2000, blank=True, null=True)


class Person(AbstractUser):
    email = models.EmailField(unique=True)
    unverified_email = models.EmailField(blank=True, null=True)
    orcid = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    link = models.URLField(max_length=2000, blank=True, null=True)
    organization = models.OneToOneField(Organization, related_name='person', on_delete=models.SET_NULL,  
                                        db_column='organizationId', blank=True, null=True)
    hydroshare_token = models.JSONField(blank=True, null=True)

    objects = PersonManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


class PasswordReset(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    user = models.OneToOneField('Person', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() - self.timestamp <= timedelta(days=1)
