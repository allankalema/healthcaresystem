from django.contrib import admin
from .models import (
    AntenatalCard, PreviousObstetricHistory, 
    AntenatalProgressExamination, UltrasoundReport, 
    Prescription, Medication
)

# --------------------- INLINE MODELS ---------------------
class PreviousObstetricHistoryInline(admin.TabularInline):
    model = PreviousObstetricHistory
    extra = 1
    readonly_fields = ('created_at',)
    fields = ('pregnancy_year', 'delivery_type', 'place_of_delivery', 'baby_sex', 'birth_weight', 'immunization_status', 'created_at')


class AntenatalProgressExaminationInline(admin.TabularInline):
    model = AntenatalProgressExamination
    extra = 1
    readonly_fields = ('created_at',)
    fields = ('visit_date', 'fundal_height', 'presentation', 'fetal_heart_rate', 'urine_test_results', 'created_at')


class UltrasoundReportInline(admin.TabularInline):
    model = UltrasoundReport
    extra = 1
    readonly_fields = ('created_at',)
    fields = ('ultrasound_date', 'gestational_age', 'placenta_details', 'amniotic_fluid', 'complications', 'created_at')


class MedicationInline(admin.TabularInline):
    model = Medication
    extra = 1
    fields = ('medication_name', 'dosage', 'prescription_date')

# --------------------- MAIN ADMIN MODELS ---------------------

@admin.register(AntenatalCard)
class AntenatalCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'reg_no', 'health_unit', 'phone_no', 'age', 'district', 'next_visit', 'created_at')
    search_fields = ('name', 'reg_no', 'phone_no', 'nin')
    list_filter = ('district', 'age', 'marital_status', 'next_visit')
    inlines = [PreviousObstetricHistoryInline, AntenatalProgressExaminationInline, UltrasoundReportInline]


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'disease_condition', 'prescription_date', 'follow_up_date', 'cleared', 'cleared_date')
    list_filter = ('prescription_date', 'follow_up_date', 'cleared')
    search_fields = ('patient__username', 'doctor__username', 'disease_condition')
    inlines = [MedicationInline]
