from django.contrib import admin
from .models import (
    AntenatalCard,
    PreviousObstetricHistory,
    AntenatalProgressExamination,
    UltrasoundReport,
    Prescription,
    Medication,
    Emergency
)

class AntenatalCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'reg_no', 'phone_no', 'age', 'district', 'created_at', 'updated_at')
    search_fields = ('name', 'reg_no', 'phone_no', 'nin')
    list_filter = ('marital_status', 'district', 'health_unit')
    
class PreviousObstetricHistoryAdmin(admin.ModelAdmin):
    list_display = ('antenatal_card', 'pregnancy_year', 'abortions_below_12_weeks', 'abortions_above_12_weeks', 'delivery_type', 'place_of_delivery')
    search_fields = ('antenatal_card__name', 'antenatal_card__reg_no')
    list_filter = ('pregnancy_year',)

class AntenatalProgressExaminationAdmin(admin.ModelAdmin):
    list_display = ('antenatal_card', 'visit_date', 'fundal_height', 'fetal_heart_rate', 'presentation', 'created_at')
    search_fields = ('antenatal_card__name', 'antenatal_card__reg_no')
    list_filter = ('visit_date',)

class UltrasoundReportAdmin(admin.ModelAdmin):
    list_display = ('antenatal_card', 'ultrasound_date', 'gestational_age', 'created_at')
    search_fields = ('antenatal_card__name', 'antenatal_card__reg_no')
    list_filter = ('ultrasound_date',)

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'disease_condition', 'prescription_date', 'follow_up_date', 'cleared')
    search_fields = ('patient__username', 'doctor__username', 'disease_condition')
    list_filter = ('cleared',)

class MedicationAdmin(admin.ModelAdmin):
    list_display = ('prescription', 'medication_name', 'dosage', 'prescription_date')
    search_fields = ('prescription__patient__username', 'medication_name')
    
class EmergencyAdmin(admin.ModelAdmin):
    list_display = ('antenatal_card', 'emergency_type', 'reported_at', 'resolved')
    search_fields = ('antenatal_card__name', 'antenatal_card__reg_no', 'emergency_type')
    list_filter = ('resolved',)

# Register models
admin.site.register(AntenatalCard, AntenatalCardAdmin)
admin.site.register(PreviousObstetricHistory, PreviousObstetricHistoryAdmin)
admin.site.register(AntenatalProgressExamination, AntenatalProgressExaminationAdmin)
admin.site.register(UltrasoundReport, UltrasoundReportAdmin)
admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(Medication, MedicationAdmin)
admin.site.register(Emergency, EmergencyAdmin)
