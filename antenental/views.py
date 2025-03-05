from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AntenatalCard, Prescription
from accounts.decorators import *
from django.shortcuts import render
from django.db.models import Q
from accounts.models import User  # Import your User model

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



def advanced_patient_search(request):
    query = request.GET.get('q')  # Get the search query from the URL parameters
    results = []

    if query:
        # Split the query into parts (first name, last name, email)
        parts = query.split()
        
        # Build a Q object to search for patients (is_patient=True)
        q_objects = Q(is_patient=True)  # Ensure only patients are searched
        
        # Add conditions for first name, last name, and email
        for part in parts:
            q_objects &= (Q(first_name__icontains=part) | Q(last_name__icontains=part) | Q(email__icontains=part))
        
        # Perform the search
        results = User.objects.filter(q_objects)

    return render(request, 'antenatal/advanced_patient_search.html', {'results': results, 'query': query})