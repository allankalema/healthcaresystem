import json
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, password=None, **extra_fields):
        """Create and return a regular user with given details"""
        if not username:
            raise ValueError(_('The Username field is required'))
        if not first_name:
            raise ValueError(_('The First Name field is required'))
        if not last_name:
            raise ValueError(_('The Last Name field is required'))
        if not email:
            raise ValueError(_('The Email field is required'))

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, email, password=None, **extra_fields):
        """Create and return a superuser with all permissions"""
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_doctor', True)
        extra_fields.setdefault('is_patient', True)
        extra_fields.setdefault('is_hospital', True)

        return self.create_user(username, first_name, last_name, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    nin = models.CharField(max_length=20, unique=True, null=True, blank=True)
    marital_status = models.CharField(
        max_length=20,
        choices=[('Single', 'Single'), ('Married', 'Married')],
        null=True, blank=True
    )
    contact = models.CharField(max_length=15, null=True, blank=True)

    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_hospital = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return self.username

class Doctor(models.Model):
    """Doctor model linked to the User model"""
    
    SPECIALIZATIONS = [
        ('ob_gyn', 'Obstetrician-Gynecologist (OB-GYN)'),
        ('perinatologist', 'Maternal-Fetal Medicine Specialist (Perinatologist)'),
        ('midwife', 'Midwife'),
        ('neonatologist', 'Neonatologist'),
        ('fertility_specialist', 'Fertility Specialist (Reproductive Endocrinologist)'),
        ('family_medicine', 'Family Medicine Doctor'),
        ('gp_maternal', 'General Practitioner (GP) with Maternal Focus'),
    ]
    
    EDUCATION_LEVELS = [
        ('certificate', 'Certificate'),
        ('diploma', 'Diploma'),
        ('bachelors', 'Bachelors'),
        ('masters', 'Masters'),
        ('phd', 'PhD'),
    ]

    RANKS = [
        ('intern', 'Intern'),
        ('junior_doctor', 'Junior Doctor'),
        ('senior_doctor', 'Senior Doctor'),
        ('consultant', 'Consultant'),
        ('specialist', 'Specialist'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    license_number = models.CharField(max_length=50, unique=True)
    specializations = models.ManyToManyField('Specialization', related_name='doctors')
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVELS)
    rank = models.CharField(max_length=20, choices=RANKS)
    available_hours = models.JSONField(default=dict)  # Example: { "Mon": "9AM-5PM", "Tue": "10AM-4PM" }

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"

class Specialization(models.Model):
    """Model to store doctor specializations"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
