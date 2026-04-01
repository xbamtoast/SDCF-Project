from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('app:home')
        else:
            # Add an error message
            messages.error(request, 'Invalid username or password.')
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('accounts:user_login')

def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('app:home')
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})