from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages



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


def enter_code(request):
    return render(request, 'accounts/enter_code.html') 

def forgot_password(request):
    return render(request, 'accounts/forgot_password.html') 

def reset_password(request):
    return render(request, 'accounts/reset_password.html') 
