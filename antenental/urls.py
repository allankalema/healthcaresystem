from django.urls import path
from . import views

urlpatterns = [
    path('antenatal-card/<int:card_id>/', views.antenatal_card_details, name='antenatal_card_details'),
    path('prescription/<int:prescription_id>/', views.prescription_details, name='prescription_details'),
]