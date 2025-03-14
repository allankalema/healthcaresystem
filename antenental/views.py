from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AntenatalCard, Prescription
from accounts.decorators import *
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render
from django.utils.timezone import now
from django.db.models import Q
from .models import *
from django.db.models import Exists, OuterRef
from.forms import *
import random
import string
from django.conf import settings
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


@login_required
def my_prescriptions(request):
    # Fetch prescriptions for the logged-in patient
    prescriptions = Prescription.objects.filter(patient=request.user)
    return render(request, 'antenatal/my_prescriptions.html', {
        'prescriptions': prescriptions,
    })

@login_required
def unadmit_patient(request, card_id):
    antenatal_card = get_object_or_404(AntenatalCard, id=card_id)

    # Ensure only the assigned doctor can unadmit the patient
    if antenatal_card.Doctor != request.user:
        messages.error(request, "You do not have permission to unadmit this patient.")
        return redirect('doctor_patients')

    # Set the patient as unadmitted
    patient = get_object_or_404(Patient, user=antenatal_card.user)
    antenatal_card.admitted = False
    antenatal_card.save()  # Save the antenatal card to reflect the changes

    messages.success(request, "Patient has been unadmitted successfully.")
    return redirect('doctor_patients')

@login_required
def readmit_patient(request, card_id):
    antenatal_card = get_object_or_404(AntenatalCard, id=card_id)

    # Ensure only the assigned doctor can readmit the patient
    if antenatal_card.Doctor != request.user:
        messages.error(request, "You do not have permission to readmit this patient.")
        return redirect('doctor_patients')

    # Set the patient as admitted
    antenatal_card.admitted = True
    antenatal_card.save()  # Save the antenatal card to reflect the changes

    messages.success(request, "Patient has been readmitted successfully.")
    return redirect('doctor_patients')



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

        # Exclude patients who have already been admitted by this doctor
        admitted_patients = AntenatalCard.objects.filter(
            user=OuterRef('id'),  # Match the patient in User model
            Doctor=request.user  # Ensure they were admitted by the logged-in doctor
        )


    return render(request, 'antenatal/advanced_patient_search.html', {'results': results, 'query': query})





def generate_random_string(length=10):
    """Generate a random string of fixed length."""
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

def admit_patient(request, patient_id):
    # Get the patient object
    patient = get_object_or_404(User, id=patient_id, is_patient=True)
    location = Location.objects.get(user=patient)
    patient_profile = Patient.objects.get(user=patient)

    if request.method == 'POST':
        # Update the User model
        patient.contact = request.POST.get('contact')
        patient.health_insurance_details = request.POST.get('health_insurance_details')
        patient.government_scheme_eligibility = request.POST.get('government_scheme_eligibility')
        patient.save()

        # Update the Patient model
        patient_profile.number_of_children = request.POST.get('number_of_children')
        patient_profile.date_of_last_period = request.POST.get('date_of_last_period')
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

        # Auto-generate health_unit and reg_no
        health_unit = "Health Unit " + generate_random_string(5)  # Example: "Health Unit Abc12"
        reg_no = "REG" + generate_random_string(7)  # Example: "REG123Abc"

        # Create an AntenatalCard instance
        antenatal_card = AntenatalCard(
            user=patient,
            Doctor=request.user,
            health_unit=health_unit,  # Auto-generated health unit
            reg_no=reg_no,  # Auto-generated registration number
            name=f"{patient.first_name} {patient.last_name}",
            nin=patient.nin,
            phone_no=request.POST.get('phone_no'),
            age=patient_profile.age,
            village=location.village,
            parish=location.parish,
            sub_county=location.sub_county,
            district=location.district,
            occupation=patient_profile.occupation,
            religion=request.POST.get('religion'),  # New field
            education_level=request.POST.get('education_level'),  # New field
            tribe=request.POST.get('tribe'),  # New field
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
            hospitalization=request.POST.get('hospitalization') == 'True',
            hospitalization_reason=request.POST.get('hospitalization_reason'),
            next_visit=request.POST.get('next_visit'),
            admitted = True
        )
        antenatal_card.save()

        # Add success message
        messages.success(request, f"{patient.first_name} {patient.last_name} has been admitted successfully and is now your patient.")
        return redirect('doctor_patients')  # Redirect to the doctor dashboard
    # Render the admission form
    return render(request, 'antenatal/admit_patient.html', {
        'patient': patient,
        'location': location,
        'patient_profile': patient_profile,
    })


def doctor_patients(request):
    # Fetch all AntenatalCard instances where the Doctor is the logged-in user
    admitted_patients = AntenatalCard.objects.filter(Doctor=request.user, admitted=True)
    unadmitted_patients = AntenatalCard.objects.filter(Doctor=request.user,admitted=False)

    # Handle search query
    search_query = request.GET.get('q')
    if search_query:
        admitted_patients = admitted_patients.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )
        unadmitted_patients = unadmitted_patients.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )

    # Render the template with separate lists
    return render(request, 'antenatal/doctor_patients.html', {
        'admitted_patients': admitted_patients,
        'unadmitted_patients': unadmitted_patients,
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



def add_information(request, patient_id):
    # Fetch the AntenatalCard instance for the patient
    antenatal_card = get_object_or_404(AntenatalCard, id=patient_id)

    if request.method == 'POST':
        # Update AntenatalCard fields
        if 'update_antenatal_card' in request.POST:
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
        'patient': antenatal_card.user,
    })



@login_required
def prescribe_medication(request):
    antenatal_cards = AntenatalCard.objects.filter(Doctor=request.user)
    selected_patient = None

    # Handle patient search
    search_query = request.GET.get('search', '')
    if search_query:
        antenatal_cards = antenatal_cards.filter(
            user__first_name__icontains=search_query
        ) | antenatal_cards.filter(
            user__last_name__icontains=search_query
        ) | antenatal_cards.filter(
            user__email__icontains=search_query
        )

    # Handle form submission
    if request.method == 'POST':
        prescription_form = PrescriptionForm(request.POST)
        medication_formset = MedicationFormSet(request.POST)

        if prescription_form.is_valid() and medication_formset.is_valid():
            # Save prescription
            prescription = prescription_form.save(commit=False)
            prescription.patient = User.objects.get(id=request.POST.get('patient'))
            prescription.doctor = request.user
            prescription.save()

            # Save medications
            for form in medication_formset:
                if form.cleaned_data.get('medication_name'):
                    medication = form.save(commit=False)
                    medication.prescription = prescription
                    medication.save()

            # Send email to the patient
            send_mail(
                subject="New Prescription",
                message=f"You have a new prescription from Dr. {request.user.get_full_name()}. "
                        f"Please log in to the system for more details.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[prescription.patient.email],
                fail_silently=False,
            )

            messages.success(request, "Prescription created successfully!")
            return redirect('doctor_dashboard')
        else:
            messages.error(request, "Error creating prescription. Please check the form.")
    else:
        prescription_form = PrescriptionForm()
        medication_formset = MedicationFormSet()

    return render(request, 'prescription/prescribe_medication.html', {
        'antenatal_cards': antenatal_cards,
        'prescription_form': prescription_form,
        'medication_formset': medication_formset,
        'search_query': search_query,
    })


@login_required
def send_notification(request):
    if request.method == 'POST':
        header = request.POST.get('header')
        body = request.POST.get('body')
        send_by = request.POST.get('send_by')

        if send_by == 'location':
            # Get location filters
            village = request.POST.get('village')
            parish = request.POST.get('parish')
            sub_county = request.POST.get('sub_county')
            district = request.POST.get('district')

            # Build a dynamic query using Q objects
            location_filters = Q()
            if village:
                location_filters |= Q(village=village)
            if parish:
                location_filters |= Q(parish=parish)
            if sub_county:
                location_filters |= Q(sub_county=sub_county)
            if district:
                location_filters |= Q(district=district)

            # Filter locations based on the dynamic query
            locations = Location.objects.filter(location_filters)

            # Filter patients whose location matches any of the filtered locations
            patients = User.objects.filter(
                is_patient=True,
                location__in=locations
            )

            # Send emails to filtered patients
            for patient in patients:
                send_mail(
                    subject=header,
                    message=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[patient.email],
                    fail_silently=False,
                )

            messages.success(request, f"Notification sent to {patients.count()} patients.")
            return redirect('doctor_dashboard')

        elif send_by == 'email':
            # Send to a specific email
            email = request.POST.get('email')
            send_mail(
                subject=header,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, f"Notification sent to {email}.")
            return redirect('doctor_dashboard')

    return render(request, 'notification/send_notification.html')


@login_required
def emergency_list(request):
    # Fetch emergencies for patients assigned to the logged-in doctor
    emergencies = Emergency.objects.filter(
        antenatal_card__Doctor=request.user
    ).select_related('antenatal_card__user')

    return render(request, 'emergency/emergency_list.html', {
        'emergencies': emergencies,
    })

@login_required
def emergency_detail(request, emergency_id):
    # Fetch the specific emergency
    emergency = get_object_or_404(Emergency, id=emergency_id, antenatal_card__Doctor=request.user)
    return render(request, 'emergency/emergency_detail.html', {
        'emergency': emergency,
    })


@login_required
def report_emergency(request):
    # Get the patient's antenatal card
    antenatal_card = AntenatalCard.objects.filter(user=request.user).first()

    if not antenatal_card:
        messages.error(request, "You do not have an antenatal card.")
        return redirect('patient_dashboard')

    if request.method == 'POST':
        form = EmergencyForm(request.POST)
        if form.is_valid():
            # Save the emergency
            emergency = form.save(commit=False)
            emergency.antenatal_card = antenatal_card
            emergency.reported_by = request.user
            emergency.save()

            # Send email to the assigned doctor
            doctor = antenatal_card.Doctor
            send_mail(
                subject=f"Emergency Reported by {request.user.get_full_name()}",
                message=f"A new emergency has been reported by {request.user.get_full_name()}.\n\n"
                        f"Emergency Type: {emergency.emergency_type}\n"
                        f"Description: {emergency.description}\n\n"
                        f"Please take appropriate action.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[doctor.email],
                fail_silently=False,
            )

            messages.success(request, "Emergency reported successfully. Your doctor has been notified.")
            return redirect('patient_dashboard')
    else:
        form = EmergencyForm()

        

    return render(request, 'emergency/report_emergency.html', {
        'form': form,
    })

def previous_obstetric_history_detail(request, history_id):
    history = get_object_or_404(PreviousObstetricHistory, id=history_id)
    return render(request, 'antenatal/previous_obstetric_history_detail.html', {
        'history': history,
    })

def antenatal_progress_detail(request, progress_id):
    progress = get_object_or_404(AntenatalProgressExamination, id=progress_id)
    return render(request, 'antenatal/antenatal_progress_detail.html', {
        'progress': progress,
    })

def ultrasound_report_detail(request, report_id):
    report = get_object_or_404(UltrasoundReport, id=report_id)
    return render(request, 'antenatal/ultrasound_report_detail.html', {
        'report': report,
    })