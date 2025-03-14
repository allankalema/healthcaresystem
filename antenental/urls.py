from django.urls import path
from . import views

urlpatterns = [
    path('antenatal-card/<int:card_id>/', views.antenatal_card_details, name='antenatal_card_details'),
    path('prescription/<int:prescription_id>/', views.prescription_details, name='prescription_details'),
    path('my-prescriptions/',views.my_prescriptions, name='my_prescriptions'),
    path('advanced-patient-search/', views.advanced_patient_search, name='advanced_patient_search'),
    path('admit-patient/<int:patient_id>/', views.admit_patient, name='admit_patient'),
    path('doctor-patients/', views.doctor_patients, name='doctor_patients'),
    path('patient-details/<int:patient_id>/', views.patient_details, name='patient_details'),
    path('add-information/<int:patient_id>/', views.add_information, name='add_information'),
    path('prescribe/', views.prescribe_medication, name='prescribe_medication'),
    path('send-notification/', views.send_notification, name='send_notification'),
    path('emergencies/', views.emergency_list, name='emergency_list'),
    path('emergencies/<int:emergency_id>/', views.emergency_detail, name='emergency_detail'),
     path('report-emergency/', views.report_emergency, name='report_emergency'),
     path('previous-obstetric-history/<int:history_id>/', views.previous_obstetric_history_detail, name='previous_obstetric_history_detail'),
    path('antenatal-progress/<int:progress_id>/', views.antenatal_progress_detail, name='antenatal_progress_detail'),
    path('ultrasound-report/<int:report_id>/', views.ultrasound_report_detail, name='ultrasound_report_detail'),

]