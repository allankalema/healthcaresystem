from django.shortcuts import render

def base(request):
    return render(request, 'home.html') 

def login(request):
    return render(request, 'accounts/login.html') 
