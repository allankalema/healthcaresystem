from django.contrib.auth import authenticate, login
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from antenental.models import *
from django.utils import timezone 

def forbidden_view(request):
    """View for handling forbidden access attempts."""
    return render(request, '403.html', status=403)


def base(request):
    return render(request, 'home.html') 

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful! Welcome back.")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, "accounts/login.html")


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Please proceed to the next step.')
            return redirect('additional_details', user_id=user.id)  # Redirect to additional details page
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})


def doctor_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Please proceed to the next step.')
            return redirect('doctor_additional_details', user_id=user.id)  # Redirect to additional details page
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def additional_details(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        location_form = LocationForm(request.POST)
        patient_form = PatientForm(request.POST)
        if location_form.is_valid() and patient_form.is_valid():
            # Save location
            location = location_form.save(commit=False)
            location.user = user
            location.save()

            # Save patient details
            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()

            # Update user role to patient
            user.is_patient = True
            user.save()

            messages.success(request, 'Additional details saved successfully!')
            return redirect('home')
        else:
            # Display form errors
            for field, errors in location_form.errors.items():
                for error in errors:
                    messages.error(request, f"Location - {field}: {error}")
            for field, errors in patient_form.errors.items():
                for error in errors:
                    messages.error(request, f"Patient - {field}: {error}")
    else:
        location_form = LocationForm()
        patient_form = PatientForm()

    return render(request, 'accounts/additional_details.html', {
        'location_form': location_form,
        'patient_form': patient_form,
    })





@login_required
def doctor_additional_details(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        location_form = LocationForm(request.POST)
        doctor_form = DoctorForm(request.POST)
        if location_form.is_valid() and doctor_form.is_valid():
            # Save location
            location = location_form.save(commit=False)
            location.user = user
            location.save()

            # Save doctor details
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()

            # Update user role to doctor
            user.is_doctor = True
            user.save()

            messages.success(request, 'Additional details saved successfully!')
            return redirect('home')
        else:
            # Display form errors
            for field, errors in location_form.errors.items():
                for error in errors:
                    messages.error(request, f"Location - {field}: {error}")
            for field, errors in doctor_form.errors.items():
                for error in errors:
                    messages.error(request, f"Doctor - {field}: {error}")
    else:
        location_form = LocationForm()
        doctor_form = DoctorForm()

    return render(request, 'accounts/doctor_additional_details.html', {
        'location_form': location_form,
        'doctor_form': doctor_form,
    })



def enter_code(request):
    return render(request, 'accounts/enter_code.html') 

def forgot_password(request):
    return render(request, 'accounts/forgot_password.html') 

def reset_password(request):
    return render(request, 'accounts/reset_password.html') 

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()  # Change the password
            update_session_auth_hash(request, form.user)  # Keep the user logged in after password change
            messages.success(request, 'Your password has been updated successfully!')
            return redirect('home')  # Redirect to home after success
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})


@login_required
def user_logout(request):
    # Log the user out
    logout(request)
    
    # Add a success message
    messages.success(request, 'You have successfully logged out.')
    
    # Redirect to the login page
    return redirect('login')


@login_required
def profile_update(request):
    user = request.user
    location, _ = Location.objects.get_or_create(user=user)
    patient, _ = Patient.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        location_form = LocationUpdateForm(request.POST, instance=location)
        patient_form = PatientUpdateForm(request.POST, instance=patient)

        if user_form.is_valid() and location_form.is_valid() and patient_form.is_valid():
            user_form.save()
            location_form.save()
            patient_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('home')
        else:
            # Display form errors
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f"User - {field}: {error}")
            for field, errors in location_form.errors.items():
                for error in errors:
                    messages.error(request, f"Location - {field}: {error}")
            for field, errors in patient_form.errors.items():
                for error in errors:
                    messages.error(request, f"Patient - {field}: {error}")
    else:
        user_form = UserUpdateForm(instance=user)
        location_form = LocationUpdateForm(instance=location)
        patient_form = PatientUpdateForm(instance=patient)

    return render(request, 'accounts/profile_update.html', {
        'user_form': user_form,
        'location_form': location_form,
        'patient_form': patient_form,
    })



@login_required
def doctor_profile_update(request):
    user = request.user
    location, _ = Location.objects.get_or_create(user=user)
    doctor, _ = Doctor.objects.get_or_create(user=user)

    if request.method == 'POST':
        location_form = LocationUpdateForm(request.POST, instance=location)
        doctor_form = DoctorUpdateForm(request.POST, instance=doctor)

        if location_form.is_valid() and doctor_form.is_valid():
            location_form.save()
            doctor_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('home')
        else:
            # Display form errors
            for field, errors in location_form.errors.items():
                for error in errors:
                    messages.error(request, f"Location - {field}: {error}")
            for field, errors in doctor_form.errors.items():
                for error in errors:
                    messages.error(request, f"Doctor - {field}: {error}")
    else:
        location_form = LocationUpdateForm(instance=location)
        doctor_form = DoctorUpdateForm(instance=doctor)

    return render(request, 'accounts/doctor_profile_update.html', {
        'location_form': location_form,
        'doctor_form': doctor_form,
    })




@login_required
@patient
def patient_dashboard(request):
    user = request.user

    # Fetch patient, location, and antenatal card data
    patient = Patient.objects.filter(user=user).first()
    location = Location.objects.filter(user=user).first()
    antenatal_card = AntenatalCard.objects.filter(user=user).first()
    prescriptions = Prescription.objects.filter(patient=user).order_by('-prescription_date')

    # Pass the next_visit date to the template
    next_visit_date = antenatal_card.next_visit if antenatal_card else None

    context = {
        'patient': patient,
        'location': location,
        'antenatal_card': antenatal_card,
        'prescriptions': prescriptions,
        'next_visit_date': next_visit_date,  # Add this line
    }

    return render(request, 'dashboards/patient_dashboard.html', context)


@login_required
def doctor_dashboard(request):
    # Ensure the user is a doctor
    if not request.user.is_doctor:
        return redirect('home')  # Redirect non-doctors to the home page

    # Fetch the doctor's profile
    doctor = Doctor.objects.filter(user=request.user).first()

    # Fetch unresolved emergencies for the doctor's patients
    emergencies = Emergency.objects.filter(
        antenatal_card__Doctor=request.user,
        resolved=False
    ).select_related('antenatal_card__user')

   # Fetch next visit dates for patients assigned to this doctor
    next_visits = AntenatalCard.objects.filter(
        Doctor=request.user,
        next_visit__isnull=False,  # Only include cards with a next_visit date
        next_visit__gte=timezone.now().date()  # Only include future dates
    ).select_related('user')
    
    # Prepare data for the calendar
    calendar_events = [
        {
            'title': f"{card.user.first_name} {card.user.last_name}",  # Patient's name
            'start': card.next_visit.strftime('%Y-%m-%d'),  # Next visit date
            'backgroundColor': '#FF69B4',  # Pink background color
            'borderColor': '#FF69B4',  # Pink border color
            'textColor': '#FFFFFF',  # White text color
        }
        for card in next_visits
    ]

    context = {
        'doctor': doctor,
        'emergencies': emergencies,
        'calendar_events': calendar_events,  # Pass calendar events to the template
    }

    return render(request, 'dashboards/doctor_dashboard.html', context)

