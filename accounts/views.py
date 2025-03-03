from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PatientSignupForm


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


def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_patient = True  # Set the user as a patient
            user.save()
            messages.success(request, 'Account created successfully! Please proceed to the next step.')
            return redirect('home')  # Redirect to home or the next phase
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PatientSignupForm()

    return render(request, 'accounts/patient_signup.html', {'form': form})

    
def enter_code(request):
    return render(request, 'accounts/enter_code.html') 

def forgot_password(request):
    return render(request, 'accounts/forgot_password.html') 

def reset_password(request):
    return render(request, 'accounts/reset_password.html') 
