from django.shortcuts import render

def base(request):
    return render(request, 'home.html') 

def login(request):
    return render(request, 'accounts/login.html') 

def enter_code(request):
    return render(request, 'accounts/enter_code.html') 

def forgot_password(request):
    return render(request, 'accounts/forgot_password.html') 

def reset_password(request):
    return render(request, 'accounts/reset_password.html') 
