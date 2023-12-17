from django.shortcuts import render, redirect
from .forms import UserForm
from django.http import HttpResponse
from .models import User, UserProfile
from django.contrib import messages
from vendor.forms import VendorForm
# Create your views here.


def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.set_password(password)
            user.save()
            messages.success(request, "Your account has been registered successfully !!!")
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

            return render(request, 'register-restaurant.html', context)

    else:
        user_form = UserForm()
        context = {
            'form': user_form,
        }
        return render(request, 'register-user.html', context)

def register_vendor(request):
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
            messages.success(request, 'Your application is submitted successfully !!!')
            return redirect('register_vendor')
        else:
            context= {
                'form': form,
                'v_form': v_form,
            }

            return render(request, 'register-vendor.html', context)

    else:
        form = UserForm()
        v_form = VendorForm()
        context = {
            'form': form,
            'v_form': v_form,
        }
        return render(request, 'register-vendor.html', context)