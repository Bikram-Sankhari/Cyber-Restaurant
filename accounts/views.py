from django.shortcuts import render, redirect
from .forms import UserForm
from django.http import HttpResponse
from .models import User
from django.contrib import messages
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
        return render(request, 'register-restaurant.html', context)
