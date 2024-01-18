from django.db import IntegrityError
from django.shortcuts import render, redirect
from .forms import UserForm
from django.http import HttpResponse
from .models import User, UserProfile
from django.contrib import messages, auth
from vendor.forms import VendorForm
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .forms import UserForm
from .utils import logged_in_redirect, send_verification_email, send_password_reset_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.template.defaultfilters import slugify

# Create your views here.


def validate_customer(user):
    if user.get_role() == 'customer':
        return True
    else:
        raise PermissionDenied('You are not authorised')


def validate_vendor(user):
    if user.get_role() == 'vendor':
        return True
    else:
        raise PermissionDenied('You are not authorised')


def register_user(request):
    if request.user.is_authenticated:
        return logged_in_redirect(request, f"You are logged In as {request.user.username}.\nPlease logout first to register another user!")

    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.set_password(password)
            user.save()

            # Send Verification Email
            send_verification_email(request, user)

            messages.success(
                request, "Your account has been registered successfully !!!")
            return redirect('register_user')

        else:
            email = form['email'].value()
            try:
                obj_by_email = User.objects.get(email=email)
            except:
                obj_by_email = None

            if obj_by_email:
                messages.info(
                    request, 'Email Already Registered. Please Login to continue!')
                return redirect('login')

            context = {
                'form': form,
            }

            return render(request, 'accounts/register-user.html', context)

    else:
        user_form = UserForm()
        context = {
            'form': user_form,
        }
        return render(request, 'accounts/register-user.html', context)


def register_vendor(request):
    if request.user.is_authenticated:
        return logged_in_redirect(request, f"You are logged In as {request.user.username}.\nPlease logout first to register a restaurant!")

    if request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)

        if form.is_valid() and v_form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.role = User.RESTAURANT
            user.set_password(password)
            try:
                user.save()
            except IntegrityError:
                messages.error(request, 'Vendor already registered')
                return redirect('register_vendor')

            # Send Verification Email
            send_verification_email(request, user)

            vendor_name = v_form.cleaned_data['vendor_name']
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor.user_profile = UserProfile.objects.get(user=user)
            vendor.vendor_slug = slugify(vendor_name)
            try:
                vendor.save()
            except IntegrityError:
                messages.error(request, 'Vendor already registered')
                return redirect('register_vendor')
            
            messages.success(
                request, 'Your application is submitted successfully !!!')
            return redirect('register_vendor')
        else:
            context = {
                'form': form,
                'v_form': v_form,
            }

            return render(request, 'accounts/register-vendor.html', context)

    else:
        form = UserForm()
        v_form = VendorForm()
        context = {
            'form': form,
            'v_form': v_form,
        }
        return render(request, 'accounts/register-vendor.html', context)


def login(request):
    if request.user.is_authenticated:
        return logged_in_redirect(request, "You are already logged In !")

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user:
            auth.login(request, user)
            messages.success(request, 'You are now Logged In !!!')
            return redirect('my_account')

        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    else:
        form = UserForm()
        context = {
            'form': form,
        }
        return render(request, 'accounts/login.html', context)


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.info(request, "You have been successfully logged out")
    return redirect('login')


@login_required(login_url='login')
@user_passes_test(validate_vendor)
def vendor_dashboard(request):
    return render(request, 'accounts/vendor_dashboard.html')


@login_required(login_url='login')
@user_passes_test(validate_customer)
def customer_dashboard(request):
    return render(request, 'accounts/customer_dashboard.html')


@login_required(login_url='login')
def my_account(request):
    role = request.user.get_role()
    if role == 'vendor':
        return redirect('vendor_dashboard')
    elif role == 'customer':
        return redirect('customer_dashboard')
    elif role == 'super_admin':
        return redirect('/admin')
    else:
        return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, 'Your account has been activated successfully !')
        return redirect('my_account')

    else:
        messages.error(request, 'Invalid Link. Could not activate account !!!')
        return redirect('login')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        try:
            user = User.objects.get(email=email)
        except:
            user = None

        if user:
            send_password_reset_email(request, user)
            messages.success(request, 'Password reset mail sent to your Email')
            return redirect('forgot_password')

        else:
            messages.error(request, 'No user found with this Email ID')
            return redirect('register_user')

    else:
        return render(request, 'accounts/forgot_password.html')


def validate_forgot_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        request.session['uid'] = int(uid)
        return redirect('reset_password')
    else:
        messages.error(
            request, 'Could not verify Email. Please login to continue !!!')
        return redirect('login')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            id = request.session.get('uid')
            user = User.objects.get(pk=id)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(
                request, 'Your Password has been changed successfully. Please Login with new pasword to continue !!!!')
            return redirect('login')

        else:
            messages.error(
                request, "Password and Confirm Password do not match !")
            return redirect('reset_password')

    else:
        return render(request, 'accounts/reset_password.html')
