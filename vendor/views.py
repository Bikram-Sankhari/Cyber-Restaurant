from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import user_passes_test, login_required
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.views import validate_vendor
from menu.models import Category, FoodItem
from .models import Vendor
from .forms import VendorForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from menu.forms import CategoryForm
from .utils import get_vendor
from django.template.defaultfilters import slugify
# Create your views here.


@login_required(login_url='login')
@user_passes_test(validate_vendor)
def vendor_profile(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        user_profile_form = UserProfileForm(
            request.POST, request.FILES, instance=profile)

        if vendor_form.is_valid() and user_profile_form.is_valid():
            vendor_form.save()
            user_profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('vendor_profile')
        else:
            print(vendor_form.errors)
            print(user_profile_form.errors)

            context = {
                'vendor_form': vendor_form,
                'user_profile_form': user_profile_form,
                'profile': profile,
                'vendor': vendor,
            }

            return render(request, 'vendor/vendor_profile.html', context)
    else:
        vendor_form = VendorForm(instance=vendor)
        user_profile_form = UserProfileForm(instance=profile)
        context = {
            'vendor_form': vendor_form,
            'user_profile_form': user_profile_form,
            'profile': profile,
            'vendor': vendor,
        }
        return render(request, 'vendor/vendor_profile.html', context)

@login_required(login_url='login')
@user_passes_test(validate_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories': categories,
    }
    return render(request, 'vendor/menu_builder.html', context)


@login_required(login_url='login')
@user_passes_test(validate_vendor)
def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)
    context = {
        'fooditems': fooditems,
        'category': category,
    }
    return render(request, 'vendor/fooditems_by_category.html', context)


@login_required(login_url='login')
@user_passes_test(validate_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            try:
                category.save()
            except IntegrityError:
                messages.info(request, 'Category already exists')
            else:
                messages.success(request, f'Category - \"{category_name.upper()}\" added successfully')
            return redirect('menu_builder')
        else:
            for field in form:
                for error in field.errors:
                    print(error)
                    messages.error(request, error)
    else:
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_category.html', context)


@login_required(login_url='login')
@user_passes_test(validate_vendor)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category deleted successfully')
    return redirect('menu_builder')


@login_required(login_url='login')
@user_passes_test(validate_vendor)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if category.vendor != get_vendor(request):
        messages.error(request, 'You are not allowed to edit this category')
        return redirect('menu_builder')
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.slug = slugify(category_name)
            try:
                category.save()
            except IntegrityError:
                messages.info(request, 'A Similar Category already exists')
                return redirect('edit_category', category.pk)

            else:
                messages.success(request, 'Category updated successfully')
            return redirect('menu_builder')
        else:
            for field in form:
                for error in field.errors:
                    print(error)
                    messages.error(request, error)
    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'vendor/edit_category.html', context)