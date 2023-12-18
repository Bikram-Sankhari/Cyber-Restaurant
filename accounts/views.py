from django.shortcuts import render, redirect
from .forms import UserForm
from django.http import HttpResponse
from .models import User, UserProfile
from django.contrib import messages, auth
from vendor.forms import VendorForm
from .forms import UserForm
from .utils import logged_in_redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
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
                return HttpResponse(obj_by_email)

            context = {
                'form': form,
            }

            return render(request, 'accounts/register-restaurant.html', context)

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
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor.user_profile = UserProfile.objects.get(user=user)
            vendor.save()
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
    print(role)
    if role == 'vendor':
        return redirect('vendor_dashboard')
    elif role == 'customer':
        return redirect('customer_dashboard')
    elif role == 'super_admin':
        return redirect('/admin')
    else:
        return redirect('home')
