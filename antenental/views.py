from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AntenatalCard, Prescription
from accounts.decorators import *
from django.contrib import messages
from django.shortcuts import render
from django.utils.timezone import now
from django.db.models import Q
from .models import *
from.forms import *
from accounts.models import * # Import your User model


@login_required
@patient
def antenatal_card_details(request, card_id):
    antenatal_card = get_object_or_404(AntenatalCard, id=card_id, user=request.user)
    
    if request.method == 'POST':
        form = AntenatalCardUpdateForm(request.POST, instance=antenatal_card)
        if form.is_valid():
            form.save()
            messages.success(request, "Antenatal card updated successfully!")  # Success message
            return redirect('antenatal_card_details', card_id=card_id)
        else:
            # Debugging: Print form errors to the console
            print("Form errors:", form.errors)
            messages.error(request, "Error updating antenatal card. Please check the form.")  # Error message
    else:
        form = AntenatalCardUpdateForm(instance=antenatal_card)
    
    return render(request, 'antenatal/antenatal_card_details.html', {
        'antenatal_card': antenatal_card,
        'form': form
    })


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




def doctor_patients(request):
    # Fetch all AntenatalCard instances where the Doctor is the logged-in user
    antenatal_cards = AntenatalCard.objects.filter(Doctor=request.user)

    # Handle search query
    search_query = request.GET.get('q')
    if search_query:
        # Filter patients by first name, last name, or email
        antenatal_cards = antenatal_cards.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )

    # Render the template with the fetched data
    return render(request, 'antenatal/doctor_patients.html', {
        'antenatal_cards': antenatal_cards,
        'search_query': search_query,
    })




def patient_details(request, patient_id):
    # Fetch the AntenatalCard instance for the patient
    antenatal_card = get_object_or_404(AntenatalCard, id=patient_id)

    # Fetch related data
    previous_histories = PreviousObstetricHistory.objects.filter(antenatal_card=antenatal_card)
    progress_examinations = AntenatalProgressExamination.objects.filter(antenatal_card=antenatal_card)
    ultrasound_reports = UltrasoundReport.objects.filter(antenatal_card=antenatal_card)

    # Render the template
    return render(request, 'antenatal/patient_details.html', {
        'antenatal_card': antenatal_card,
        'previous_histories': previous_histories,
        'progress_examinations': progress_examinations,
        'ultrasound_reports': ultrasound_reports,
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import AntenatalCard, PreviousObstetricHistory, AntenatalProgressExamination, UltrasoundReport
from .forms import PreviousObstetricHistoryForm, AntenatalProgressExaminationForm, UltrasoundReportForm

def add_information(request, patient_id):
    # Fetch the AntenatalCard instance for the patient
    antenatal_card = get_object_or_404(AntenatalCard, id=patient_id)

    if request.method == 'POST':
        # Update AntenatalCard fields
        if 'update_antenatal_card' in request.POST:
            antenatal_card.gravida = request.POST.get('gravida', antenatal_card.gravida)
            antenatal_card.para = request.POST.get('para', antenatal_card.para)
            antenatal_card.abortions = request.POST.get('abortions', antenatal_card.abortions)
            antenatal_card.presenting_complaints = request.POST.get('presenting_complaints', antenatal_card.presenting_complaints)
            antenatal_card.first_day_of_lnmp = request.POST.get('first_day_of_lnmp', antenatal_card.first_day_of_lnmp)
            antenatal_card.edd = request.POST.get('edd', antenatal_card.edd)
            antenatal_card.weeks_of_amenorrhea = request.POST.get('weeks_of_amenorrhea', antenatal_card.weeks_of_amenorrhea)
            antenatal_card.complications_of_pregnancy = request.POST.get('complications_of_pregnancy', antenatal_card.complications_of_pregnancy)
            antenatal_card.hospitalization = request.POST.get('hospitalization') == 'on'
            antenatal_card.hospitalization_reason = request.POST.get('hospitalization_reason', antenatal_card.hospitalization_reason)
            antenatal_card.next_visit = request.POST.get('next_visit', antenatal_card.next_visit)
            antenatal_card.save()
            messages.success(request, 'Antenatal card updated successfully.')

            # Send email after updating the card
            send_mail(
                'Updated Visit Details',
                f'Your next visit is scheduled for {antenatal_card.next_visit}. Please check your calendar for details.',
                'no-reply@example.com',
                [antenatal_card.user.email],
                fail_silently=False,
            )

        # Add new PreviousObstetricHistory
        elif 'add_previous_obstetric_history' in request.POST:
            form = PreviousObstetricHistoryForm(request.POST)
            if form.is_valid():
                history = form.save(commit=False)
                history.antenatal_card = antenatal_card
                history.recorded_by = request.user
                history.save()
                messages.success(request, 'Previous obstetric history added successfully.')

        # Add new AntenatalProgressExamination
        elif 'add_antenatal_progress' in request.POST:
            form = AntenatalProgressExaminationForm(request.POST)
            if form.is_valid():
                progress = form.save(commit=False)
                progress.antenatal_card = antenatal_card
                progress.recorded_by = request.user
                progress.save()
                messages.success(request, 'Antenatal progress examination added successfully.')

        # Add new UltrasoundReport
        elif 'add_ultrasound_report' in request.POST:
            form = UltrasoundReportForm(request.POST)
            if form.is_valid():
                report = form.save(commit=False)
                report.antenatal_card = antenatal_card
                report.recorded_by = request.user
                report.save()
                messages.success(request, 'Ultrasound report added successfully.')

        # Redirect to the same page after saving
        return redirect('add_information', patient_id=patient_id)

    # Fetch related data
    previous_histories = PreviousObstetricHistory.objects.filter(antenatal_card=antenatal_card)
    progress_examinations = AntenatalProgressExamination.objects.filter(antenatal_card=antenatal_card)
    ultrasound_reports = UltrasoundReport.objects.filter(antenatal_card=antenatal_card)

    # Render the template
    return render(request, 'antenatal/add_information.html', {
        'antenatal_card': antenatal_card,
        'previous_histories': previous_histories,
        'progress_examinations': progress_examinations,
        'ultrasound_reports': ultrasound_reports,
        'previous_obstetric_history_form': PreviousObstetricHistoryForm(),
        'antenatal_progress_form': AntenatalProgressExaminationForm(),
        'ultrasound_report_form': UltrasoundReportForm(),
    })