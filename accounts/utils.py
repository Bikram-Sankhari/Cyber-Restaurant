from django.contrib import messages
from django.shortcuts import redirect

def logged_in_redirect(request, message):
    messages.warning(request, message)
    return redirect('my_account')