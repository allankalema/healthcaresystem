from django.contrib import admin
from .models import User, Location, Patient, Doctor, Hospital


# ----------------------- USER ADMIN -----------------------
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_doctor', 'is_patient', 'is_hospital', 'is_active', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('is_doctor', 'is_patient', 'is_hospital', 'is_active', 'is_staff')
    ordering = ('-created_at',)
    
    # Fields to exclude
    exclude = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'nin', 'marital_status', 'contact', 'health_insurance_details', 'government_scheme_eligibility')
        }),
        ('Role-based Details', {
            'fields': ('is_doctor', 'is_patient', 'is_hospital', 'is_active', 'is_staff')
        }),
    )


# ----------------------- LOCATION ADMIN -----------------------
class LocationAdmin(admin.ModelAdmin):
    list_display = ('user', 'village', 'parish', 'sub_county', 'district')
    search_fields = ('user__username', 'village', 'parish', 'sub_county', 'district')
    list_filter = ('district',)

    # Include the user field in the form for the admin panel
    fieldsets = (
        (None, {
            'fields': ('user', 'village', 'parish', 'sub_county', 'district', 'address')
        }),
    )


# ----------------------- PATIENT ADMIN -----------------------
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'occupation', 'gestational_age', 'expected_due_date')
    search_fields = ('user__username', 'occupation')
    list_filter = ('gestational_age', 'expected_due_date')

    # Include the user field in the form for the admin panel
    fieldsets = (
        (None, {
            'fields': ('user', 'age', 'occupation', 'gestational_age', 'expected_due_date', 'type_of_pregnancy', 'previous_pregnancies', 'delivery_history', 'high_risk_factors', 'fetal_health')
        }),
    )


# ----------------------- DOCTOR ADMIN -----------------------
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'certificate_number', 'contact_number', 'health_facility', 'medical_field', 'experience_years')
    search_fields = ('user__username', 'certificate_number', 'medical_field')
    list_filter = ('experience_years', 'medical_field')

    # Include the user field in the form for the admin panel
    fieldsets = (
        (None, {
            'fields': ('user', 'certificate_number', 'contact_number', 'health_facility', 'medical_field', 'experience_years', 'education_level', 'rank_title')
        }),
    )


# ----------------------- HOSPITAL ADMIN -----------------------
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'bed_availability', 'maternity_ward_occupancy', 'ambulance_response_time')
    search_fields = ('user__username', 'name')
    list_filter = ('bed_availability', 'maternity_ward_occupancy')

    # Include the user field in the form for the admin panel
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'rank_reviews', 'departments', 'bed_availability', 'maternity_ward_occupancy', 'ambulance_response_time', 'specialized_maternity_care', 'delivery_facilities', 'blood_bank_availability', 'room_types_facilities', 'infection_control_measures', 'delivery_package_costs', 'insurance_coverage', 'government_schemes_supported')
        }),
    )


# Registering models and their respective admins
admin.site.register(User, UserAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Hospital, HospitalAdmin)
