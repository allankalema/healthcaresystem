from django.contrib import admin
from .models import (
    AntenatalCard, PreviousObstetricHistory, AntenatalProgressExamination,
    UltrasoundReport, Prescription, Medication, Emergency
)

@admin.register(AntenatalCard)
class AntenatalCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'reg_no', 'user', 'Doctor', 'health_unit', 'created_at')
    search_fields = ('name', 'reg_no', 'user__username', 'Doctor__username')
    list_filter = ('created_at', 'district', 'marital_status')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(PreviousObstetricHistory)
class PreviousObstetricHistoryAdmin(admin.ModelAdmin):
    list_display = ('antenatal_card', 'pregnancy_year', 'delivery_type', 'baby_sex', 'created_at')
    search_fields = ('antenatal_card__name', 'pregnancy_year')
    list_filter = ('pregnancy_year', 'delivery_type', 'baby_sex')
    readonly_fields = ('created_at',)

@admin.register(AntenatalProgressExamination)
class AntenatalProgressExaminationAdmin(admin.ModelAdmin):
    list_display = ('antenatal_card', 'visit_date', 'fundal_height', 'fetal_heart_rate', 'created_at')
    search_fields = ('antenatal_card__name', 'visit_date')
    list_filter = ('visit_date', 'fetal_heart_rate')
    readonly_fields = ('created_at',)

@admin.register(UltrasoundReport)
class UltrasoundReportAdmin(admin.ModelAdmin):
    list_display = ('antenatal_card', 'ultrasound_date', 'gestational_age', 'created_at')
    search_fields = ('antenatal_card__name', 'ultrasound_date')
    list_filter = ('ultrasound_date', 'gestational_age')
    readonly_fields = ('created_at',)

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'disease_condition', 'prescription_date', 'cleared')
    search_fields = ('patient__username', 'doctor__username', 'disease_condition')
    list_filter = ('prescription_date', 'cleared')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('prescription', 'medication_name', 'dosage', 'prescription_date')
    search_fields = ('prescription__patient__username', 'medication_name')
    list_filter = ('prescription_date',)
    readonly_fields = ('prescription_date',)

@admin.register(Emergency)
class EmergencyAdmin(admin.ModelAdmin):
    list_display = ('antenatal_card', 'emergency_type', 'reported_at', 'resolved')
    search_fields = ('antenatal_card__name', 'emergency_type')
    list_filter = ('reported_at', 'resolved')
    readonly_fields = ('reported_at', 'created_at', 'updated_at')