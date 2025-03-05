from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AntenatalCard, Prescription
from accounts.decorators import *
from django.contrib import messages
from django.shortcuts import render
from django.utils.timezone import now
from django.db.models import Q
from .models import AntenatalCard
from.forms import *
from accounts.models import * # Import your User model


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
    location = Location.objects.get(user=patient)
    patient_profile = Patient.objects.get(user=patient)

    if request.method == 'POST':
        # Update the Patient model
        patient_profile.gestational_age = request.POST.get('gestational_age')
        patient_profile.expected_due_date = request.POST.get('expected_due_date')
        patient_profile.type_of_pregnancy = request.POST.get('type_of_pregnancy')
        patient_profile.previous_pregnancies = request.POST.get('previous_pregnancies')
        patient_profile.delivery_history = request.POST.get('delivery_history')
        patient_profile.high_risk_factors = request.POST.get('high_risk_factors')
        patient_profile.fetal_health = request.POST.get('fetal_health')
        patient_profile.pre_existing_conditions = request.POST.get('pre_existing_conditions')
        patient_profile.previous_surgeries = request.POST.get('previous_surgeries')
        patient_profile.current_medications = request.POST.get('current_medications')
        patient_profile.allergies = request.POST.get('allergies')
        patient_profile.blood_type = request.POST.get('blood_type')
        patient_profile.family_medical_history = request.POST.get('family_medical_history')
        patient_profile.diet_preferences = request.POST.get('diet_preferences')
        patient_profile.exercise_level = request.POST.get('exercise_level')
        patient_profile.smoking_alcohol_drug_use = request.POST.get('smoking_alcohol_drug_use')
        patient_profile.mental_health_status = request.POST.get('mental_health_status')
        patient_profile.save()

        # Create an AntenatalCard instance
        antenatal_card = AntenatalCard(
            user=patient,
            Doctor=request.user,
            health_unit=request.POST.get('health_unit'),
            reg_no=request.POST.get('reg_no'),
            name=f"{patient.first_name} {patient.last_name}",
            nin=patient.nin,
            phone_no=patient.contact,
            age=patient_profile.age,
            village=location.village,
            parish=location.parish,
            sub_county=location.sub_county,
            district=location.district,
            occupation=patient_profile.occupation,
            marital_status=patient.marital_status,
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
        messages.success(request, f"{patient.first_name} {patient.last_name} has been admitted successfully and is now your patient.")
        return redirect('doctor_dashboard')  # Redirect to the doctor dashboard

    # Render the admission form
    return render(request, 'antenatal/admit_patient.html', {
        'patient': patient,
        'location': location,
        'patient_profile': patient_profile,
    })