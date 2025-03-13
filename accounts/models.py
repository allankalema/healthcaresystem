from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _


# ----------------------- USER MANAGER -----------------------
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


# ----------------------- USER MODEL -----------------------
class User(AbstractBaseUser, PermissionsMixin):
    """
    Central user model shared across doctors, patients, and hospitals.
    """
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    # Common Details
    date_of_birth = models.DateField(null=True, blank=True)
    nin = models.CharField(max_length=20, unique=True, null=True, blank=True)
    marital_status = models.CharField(
        max_length=20,
        choices=[('Single', 'Single'), ('Married', 'Married')],
        null=True, blank=True
    )
    contact = models.CharField(max_length=15, null=True, blank=True)
    health_insurance_details = models.TextField(null=True, blank=True)
    government_scheme_eligibility = models.TextField(null=True, blank=True)

    # Role-based Flags
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_hospital = models.BooleanField(default=False)

    # System Fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def get_full_name(self):
        """Returns the full name of the user."""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Returns the first name of the user."""
        return self.first_name

    def __str__(self):
        return self.username

class PasswordResetCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=7)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    
# ----------------------- LOCATION MODEL -----------------------
class Location(models.Model):
    """
    Stores location details for users (patients, doctors, hospitals).
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="location")
    village = models.CharField(max_length=255, null=True, blank=True)
    parish = models.CharField(max_length=255, null=True, blank=True)
    sub_county = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)  # Generic address field

    def __str__(self):
        return f"Location for {self.user.username}"


# ----------------------- PATIENT MODEL -----------------------
class Patient(models.Model):
    """
    Stores patient-specific details.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")
    age = models.IntegerField(null=True, blank=True)
    home_address = models.TextField(null=True, blank=True)
    number_of_children = models.IntegerField(null=True, blank=True)
    date_of_last_period = models.DateField(null=True, blank=True)
    occupation = models.CharField(max_length=255, null=True, blank=True)

    # Pregnancy & Medical History
    gestational_age = models.IntegerField(null=True, blank=True)  # Weeks of pregnancy
    expected_due_date = models.DateField(null=True, blank=True)
    type_of_pregnancy = models.CharField(max_length=20, choices=[('Single', 'Single'), ('Twins', 'Twins'), ('Multiples', 'Multiples')], null=True, blank=True)
    previous_pregnancies = models.IntegerField(null=True, blank=True)
    delivery_history = models.TextField(null=True, blank=True)
    high_risk_factors = models.TextField(null=True, blank=True)
    fetal_health = models.TextField(null=True, blank=True)

    # Medical History
    pre_existing_conditions = models.TextField(null=True, blank=True)
    previous_surgeries = models.TextField(null=True, blank=True)
    current_medications = models.TextField(null=True, blank=True)
    allergies = models.TextField(null=True, blank=True)
    blood_type = models.CharField(max_length=5, null=True, blank=True)
    family_medical_history = models.TextField(null=True, blank=True)

    # Lifestyle
    diet_preferences = models.TextField(null=True, blank=True)
    exercise_level = models.TextField(null=True, blank=True)
    smoking_alcohol_drug_use = models.TextField(null=True, blank=True)
    mental_health_status = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Patient Profile: {self.user.username}"


# ----------------------- DOCTOR MODEL -----------------------
class Doctor(models.Model):
    """
    Stores doctor-specific details.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    work_address = models.TextField(null=True, blank=True)
    certificate_number = models.CharField(max_length=100, unique=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    health_facility = models.CharField(max_length=255, null=True, blank=True)
    medical_field = models.CharField(max_length=255, null=True, blank=True)
    experience_years = models.IntegerField(null=True, blank=True)
    education_level = models.CharField(max_length=255, null=True, blank=True)
    rank_title = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"


# ----------------------- HOSPITAL MODEL -----------------------
class Hospital(models.Model):
    """
    Stores hospital-specific details.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="hospital_profile")
    name = models.CharField(max_length=255, unique=True)
    rank_reviews = models.TextField(null=True, blank=True)
    departments = models.TextField(null=True, blank=True)
    bed_availability = models.IntegerField(null=True, blank=True)
    maternity_ward_occupancy = models.IntegerField(null=True, blank=True)
    number_of_healthcare_professionals = models.IntegerField(null=True, blank=True)
    ambulance_response_time = models.CharField(max_length=255, null=True, blank=True)
    specialized_maternity_care = models.TextField(null=True, blank=True)
    delivery_facilities = models.TextField(null=True, blank=True)
    blood_bank_availability = models.BooleanField(default=False)
    room_types_facilities = models.TextField(null=True, blank=True)
    infection_control_measures = models.TextField(null=True, blank=True)
    delivery_package_costs = models.TextField(null=True, blank=True)
    insurance_coverage = models.TextField(null=True, blank=True)
    government_schemes_supported = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Hospital: {self.name}"
