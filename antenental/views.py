from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AntenatalCard, Prescription
from accounts.decorators import *

@login_required
@patient
def antenatal_card_details(request, card_id):
    antenatal_card = get_object_or_404(AntenatalCard, id=card_id, user=request.user)
    return render(request, 'antenatal/antenatal_card_details.html', {'antenatal_card': antenatal_card})


@login_required
@patient
def prescription_details(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id, patient=request.user)
    return render(request, 'antenatal/prescription_details.html', {'prescription': prescription})