# Import necessary modules and functions
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from ..models import *
from typing import Optional
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
import logging

# Create a logger instance
logger = logging.getLogger(__name__)

def check_login(request):
    return {
        'loggedin': request.user.is_authenticated,
        'user': request.user
    }

# Home view for Thai language
def Home_th(request):
    # Render logged in home
    logged_in = check_login(request)
    return render(request, 'public/home-th.html', logged_in)

# Home view for English language
def Home_en(request):
    logged_in = check_login(request)
    return render(request, 'home-en.html', logged_in)

# Login view with CSRF protection
@csrf_protect
def LoginView(request):
    if request.method == "POST":
        # Get username, password, and remember me Checkbox from POST request
        username: str = request.POST.get("username", "")
        password: str = request.POST.get("password", "")
        remember: Optional[str] = request.POST.get("remember")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Remember me checkbox logic
            if remember:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)  # Browser close
                
            request.session['last_login'] = timezone.now().isoformat()
            request.session['ip'] = request.META.get('REMOTE_ADDR')
            return redirect('/')
        else:
            messages.error(request, "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
            return redirect('login-th')

    return render(request, 'public/login-th.html')

# Register view
def RegisterView(request):
    if request.method == "POST":
        # Get username, email, and password from POST request
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        confirm_password = request.POST.get('confirm_password')
        user_data_has_error = False

        # Check if username or email already exists
        if CustomerUsers.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request, "ชื่อผู้ใช้นี้มีอยู่แล้ว")
        if CustomerUsers.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, "อีเมลนี้มีอยู่แล้ว")
        if len(password) < 5:
            user_data_has_error = True
            messages.error(request, "รหัสผ่านต้องมีอย่างน้อย 5 ตัวอักษร")
        if len(phone_number) != 10:
            user_data_has_error = True
            messages.error(request, "หมายเลขโทรศัพท์ต้องมี 10 หลัก")
        if password != confirm_password:
            user_data_has_error = True
            messages.error(request, "รหัสผ่านไม่ตรงกัน")
        if user_data_has_error:
            return redirect('register-th')
        else:
            # Create new user
            new_user = CustomerUsers.objects.create_user(
                email=email,
                username=username,
                password=password,
                phone_number=phone_number
            )

        messages.success(request, "สร้างบัญชีเรียบร้อยแล้ว")

    return render(request, 'public/register-th.html')

# Logout view
@login_required
def LogoutView(request):
    if request.user != None:
        logout(request)
    return redirect('/')

# Reserve view with login required
@login_required
def PrereserveView(request):
    logged_in = check_login(request)
    return render(request, 'public/resevation/pre-reservation.html', logged_in)

@login_required
def ReserveView(request):
    logged_in = check_login(request)
    return render(request, 'public/resevation/reservation.html', logged_in)

@login_required
def BigReserveView(request):  # for big
    logged_in = check_login(request)
    return render(request, 'public/resevation/big-reservation.html', logged_in)

@login_required
def MediumReserveView(request):  # for medium
    logged_in = check_login(request)
    return render(request, 'public/resevation/medium-reservation.html', logged_in)

@login_required
def SmallReserveView(request):  # for small
    logged_in = check_login(request)
    return render(request, 'public/resevation/small-reservation.html', logged_in)

# About us
def AboutusView(request):
    return render(request, 'public/aboutus.html')

# Forgot password view with GET and POST methods allowed
@csrf_protect
def ForgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            # Create PasswordReset object to reset password
            user = CustomerUsers.objects.get(email=email)
            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            # Generate password reset URL
            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})
            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

            # Email body with reset link
            email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}'

            # Create email message
            email_message = EmailMessage(
                'Reset your password',  # Email subject
                email_body,
                settings.EMAIL_HOST_USER,  # Email sender
                [email]  # Receiver email
            )
            # Set email priority headers
            email_message.extra_headers = {
                'X-Priority': '1',
                'X-MSMail-Priority': 'High',
                'Importance': 'High',
                'Priority': 'urgent'
            }
            # Continue without crashing web if sending email has an error
            email_message.fail_silently = True

            # Send email
            email_message.send()

            return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)

        except CustomerUsers.DoesNotExist:
            messages.error(request, "ไม่พบอีเมลนี้")
            return redirect('forgot-password')

    return render(request, 'public/passwordRecovery/forgot_password.html')

# Password reset sent view
def PasswordResetSent(request, reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'public/passwordRecovery/password_reset_sent.html')
    else:
        # Redirect if reset id is invalid
        messages.error(request, "ลิงก์รีเซ็ตรหัสผ่านไม่ถูกต้อง")
        return redirect('forgot-password')

# Password reset sent ---for testing---
def PasswordResetSentForTesting(request):
    return render(request, 'public/passwordRecovery/password_reset_sent.html')

# Reset password view
def ResetPassword(request, reset_id):
    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)
        if request.method == "POST":
            # Get password and confirm_password from POST request
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            passwords_have_error = False

            # Check if passwords match
            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, "รหัสผ่านไม่ตรงกัน")

            # Check if password length is sufficient
            if len(password) < 5:
                passwords_have_error = True
                messages.error(request, 'รหัสผ่านต้องมีอย่างน้อย 5 ตัวอักษร')

            # Check if reset link has expired
            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)
            if timezone.now() > expiration_time:
                passwords_have_error = True
                messages.error(request, "ลิงก์รีเซ็ตรหัสผ่านหมดอายุแล้ว")
                password_reset_id.delete()

            if not passwords_have_error:
                # Set new password for user
                user = password_reset_id.user
                user.set_password(password)
                user.save()

                # Delete password reset object
                password_reset_id.delete()

                messages.success(request, "เปลี่ยนรหัสผ่านเรียบร้อยแล้ว")
                return redirect('login-th')
            else:
                # Redirect back to password reset page and display errors
                return redirect('reset-password', reset_id=reset_id)
    # Send error and return back to forgot password page
    except PasswordReset.DoesNotExist:
        logger.warning(f"Invalid password reset attempt with reset_id: {reset_id}")
        messages.error(request, "ลิงก์รีเซ็ตรหัสผ่านไม่ถูกต้อง")
        return redirect('forgot-password')

    return render(request, 'public/passwordRecovery/reset_password.html')