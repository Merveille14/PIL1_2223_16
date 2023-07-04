from datetime import timedelta
from django.utils import timezone
import secrets
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as login_user, logout as logout_user, authenticate
from django.urls import reverse
from .models import Level, MyUser as User
from .mail import send_html_email


def anonymous_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapped_view

@anonymous_required
def login(request):

    error = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            user = authenticate(request, email=email, password=password)
            if user:
                login_user(request, user)
                return redirect('home')
            error = "User not exist, please check your credentials"
        else:
            error = "It looks like somes fields are blank"

    context = {
        'error': error,
    }

    return render(request, 'auth/login.html', context)

@anonymous_required
def register(request):

    error = None

    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        level_id = request.POST.get('level_id')

        if email and first_name and last_name and password and level_id:
            if password == confirm_password:
                if not User.objects.filter(email=email).count():
                    user = User.objects.create_user(email=email, password=password)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.level = Level.objects.get(id=level_id)
                    user.save()

                    login_user(request, user)
                    return redirect('home')
                else:
                    error = "User with the same email address already exist"
            error = "Please use the same password for confirming"
        else:
            error = "It looks like somes fields are blank"

    context = {
        'levels': Level.objects.all(),
        'error': error,
    }

    return render(request, 'auth/register.html', context)

@login_required
def logout(request):
    logout_user(request)
    return redirect('login')

@anonymous_required
def forgot_password(request):
    success, error = (None, None)

    if request.method == 'POST':
        email = request.POST.get('email')

        if email:
            if User.objects.filter(email=email).count():
                user = User.objects.get(email=email)

                token = secrets.token_urlsafe(32)
                reset_link = request.build_absolute_uri(
                    reverse('password.new', args=[token]))

                expire_at = 2
                user.reset_token = token
                user.reset_token_expiration = timezone.now() + timedelta(hours=expire_at)
                user.save()

                if send_html_email(
                    'Réinitialisation de votre mot de passe',
                    'mails/forgot-password.html',
                    {'to': user, 'reset_link': reset_link, 'expire': expire_at},
                    [email]
                ):
                    success = "Instructions for setting new password sent to your mail address, please check" 
                else:
                    error = f"Error during sending email to {email}"              
            else:
                error = "Please check egain your email address, it looks like wrong"
        else:
            error = "It looks like email field is blank"

    context = {
        'error': error,
        'success': success,
    }

    return render(request, 'auth/forgot-password.html', context)


@anonymous_required
def new_password(request, token):

    if request.method == 'POST':
        data = request.POST

        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password and confirm_password and token:
            if password == confirm_password:
                try:
                    user = User.objects.get(reset_token=token)
                    if user.is_reset_token_valid(token) and not user.is_reset_token_expired():
                        user.set_password(password)
                        user.reset_token = None
                        user.reset_token_expiration = None
                        user.save()
                        
                        success = "Your Password has successfully been changed"
                    else:
                        error = "Token Invalid"
                except User.DoesNotExist:
                    error = "Token Invalid Or Expired"
            else:
                error = "Please use same password for confirmation"
        else:
            error = "Error ! It looks like password fields are blank"
    

    context = {'token': token, 'error': error, 'success': success}

    return render(request, 'auth/new-password.html', context)
