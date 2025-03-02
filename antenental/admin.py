from django.contrib import admin
from .models import AntenatalCard, PreviousObstetricHistory, AntenatalProgressExamination, UltrasoundReport

# --------------------- INLINE MODELS ---------------------
class PreviousObstetricHistoryInline(admin.TabularInline):
    """
    Inline admin for previous obstetric history (linked to AntenatalCard).
    Allows multiple pregnancy records to be added in the AntenatalCard admin view.
    """
    model = PreviousObstetricHistory
    extra = 1  # Allows adding one additional entry at a time
    readonly_fields = ('created_at',)
    fields = ('pregnancy_year', 'delivery_type', 'place_of_delivery', 'baby_sex', 'birth_weight', 'immunization_status', 'created_at')


class AntenatalProgressExaminationInline(admin.TabularInline):
    """
    Inline admin for antenatal progress examinations (linked to AntenatalCard).
    Tracks progress of pregnancy over multiple visits.
    """
    model = AntenatalProgressExamination
    extra = 1
    readonly_fields = ('created_at',)
    fields = ('visit_date', 'fundal_height', 'presentation', 'fetal_heart_rate', 'urine_test_results', 'created_at')


class UltrasoundReportInline(admin.TabularInline):
    """
    Inline admin for ultrasound reports (linked to AntenatalCard).
    Tracks ultrasound records during pregnancy.
    """
    model = UltrasoundReport
    extra = 1
    readonly_fields = ('created_at',)
    fields = ('ultrasound_date', 'gestational_age', 'placenta_details', 'amniotic_fluid', 'complications', 'created_at')


# --------------------- MAIN ADMIN MODELS ---------------------
@admin.register(AntenatalCard)
class AntenatalCardAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Antenatal Card records.
    """
    list_display = ('name', 'reg_no', 'health_unit', 'phone_no', 'age', 'district', 'created_at')
    search_fields = ('name', 'reg_no', 'phone_no', 'nin')
    list_filter = ('district', 'created_at', 'marital_status')
    readonly_fields = ('created_at', 'updated_at')

    inlines = [PreviousObstetricHistoryInline, AntenatalProgressExaminationInline, UltrasoundReportInline]


@admin.register(PreviousObstetricHistory)
class PreviousObstetricHistoryAdmin(admin.ModelAdmin):
    """
    Admin interface for managing previous obstetric history records.
    """
    list_display = ('antenatal_card', 'pregnancy_year', 'delivery_type', 'baby_sex', 'birth_weight', 'created_at')
    search_fields = ('antenatal_card__name', 'pregnancy_year')
    list_filter = ('pregnancy_year', 'delivery_type', 'baby_sex', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(AntenatalProgressExamination)
class AntenatalProgressExaminationAdmin(admin.ModelAdmin):
    """
    Admin interface for managing antenatal progress examination records.
    """
    list_display = ('antenatal_card', 'visit_date', 'fundal_height', 'presentation', 'fetal_heart_rate', 'created_at')
    search_fields = ('antenatal_card__name', 'visit_date')
    list_filter = ('visit_date', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(UltrasoundReport)
class UltrasoundReportAdmin(admin.ModelAdmin):
    """
    Admin interface for managing ultrasound reports.
    """
    list_display = ('antenatal_card', 'ultrasound_date', 'gestational_age', 'placenta_details', 'created_at')
    search_fields = ('antenatal_card__name', 'ultrasound_date')
    list_filter = ('ultrasound_date', 'created_at')
    readonly_fields = ('created_at',)
