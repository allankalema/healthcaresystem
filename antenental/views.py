from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AntenatalCard, Prescription
from accounts.decorators import *
from django.contrib import messages
from django.shortcuts import render
from django.utils.timezone import now
from django.db.models import Q
from .models import AntenatalCard
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




def admit_patient(request, patient_id):
    # Get the patient object
    patient = get_object_or_404(User, id=patient_id, is_patient=True)
    
    if request.method == 'POST':
        # Create a new AntenatalCard instance
        antenatal_card = AntenatalCard(
            user=patient,  # Link to the patient
            Doctor=request.user,  # Link to the current doctor (request.user)
            health_unit=request.POST.get('health_unit'),
            reg_no=request.POST.get('reg_no'),
            name=f"{patient.first_name} {patient.last_name}",  # Full name
            nin=request.POST.get('nin'),
            phone_no=request.POST.get('phone_no'),
            age=request.POST.get('age'),
            village=request.POST.get('village'),
            parish=request.POST.get('parish'),
            sub_county=request.POST.get('sub_county'),
            district=request.POST.get('district'),
            occupation=request.POST.get('occupation'),
            religion=request.POST.get('religion'),
            education_level=request.POST.get('education_level'),
            tribe=request.POST.get('tribe'),
            marital_status=request.POST.get('marital_status'),
            next_of_kin_name=request.POST.get('next_of_kin_name'),
            next_of_kin_phone=request.POST.get('next_of_kin_phone'),
            next_of_kin_relationship=request.POST.get('next_of_kin_relationship'),
            next_of_kin_address=request.POST.get('next_of_kin_address'),
            gravida=request.POST.get('gravida'),
            para=request.POST.get('para'),
            abortions=request.POST.get('abortions'),
            presenting_complaints=request.POST.get('presenting_complaints'),
            first_day_of_lnmp=request.POST.get('first_day_of_lnmp'),
            edd=request.POST.get('edd'),
            weeks_of_amenorrhea=request.POST.get('weeks_of_amenorrhea'),
            complications_of_pregnancy=request.POST.get('complications_of_pregnancy'),
            hospitalization=request.POST.get('hospitalization') == 'on',
            hospitalization_reason=request.POST.get('hospitalization_reason'),
            next_visit=request.POST.get('next_visit'),
        )
        antenatal_card.save()

        # Add success message
        messages.success(request, f"{patient.first_name} {patient.last_name} has been admitted successfully.")
        return redirect('doctor_dashboard')  # Redirect to the doctor dashboard

    # Render the admission form
    return render(request, 'antenatal/admit_patient.html', {'patient': patient})