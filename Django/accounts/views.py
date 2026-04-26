from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm
from .forms import ForgotUsernameForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail

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

def password_change_internal(request):

    if request.method == 'POST':

        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # This keeps the user logged in after the password change
            update_session_auth_hash(request, user)
            return redirect('accounts:password_change_internal_success')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'misc/password_change_internal.html', {'form': form})

def password_change_internal_success(request):

    return render(request, 'misc/password_change_internal_success.html')

def forgot_username(request):
    if request.method == "POST":
        form = ForgotUsernameForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]

            users = User.objects.filter(email=email)

            if users.exists():
                usernames = [user.username for user in users]

                send_mail(
                    subject="Your Username",
                    message=f"Your username(s): {', '.join(usernames)}",
                    from_email="noreply@yourdomain.com",
                    recipient_list=[email],
                )

            # Always show same response for security
            return render(request, "forgot_username_done.html")

    else:
        form = ForgotUsernameForm()

    return render(request, "forgot_username.html", {"form": form})