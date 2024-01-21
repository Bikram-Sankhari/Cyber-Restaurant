from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings


def logged_in_redirect(request, message):
    messages.warning(request, message)
    return redirect('my_account')


def send_verification_email(request, user):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    mail_subject = f'Activation Link for Cyber Restaurant {user.get_role()} Registration'
    context = {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    }
    message = render_to_string('emails/verification_email.html', context)
    target_email = user.email

    mail = EmailMessage(mail_subject, message, from_email, to=[target_email,])
    mail.send()


def send_password_reset_email(request, user):
    from_email = settings.DEFAULT_FROM_EMAIL
    context = {
        'user': user,
        'domain': get_current_site(request),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    }
    message = render_to_string('emails/password_reset_email.html', context)
    target_email = user.email
    subject = f"Your Password Reset request for Cyber Restaurant"
    mail = EmailMessage(subject, message, from_email, to=[target_email,])
    mail.send()


def send_approval_mail(vendor):
    if vendor.is_approved:
        subject = "We are so sorry to say that you are unapproved"
    else:
        subject = "Congratulations! You're approved now...."

    context = {
        'vendor': vendor,
    }
    message = render_to_string('emails/approval_mail.html', context)
    to_mail = vendor.user.email
    mail = EmailMessage(
        subject, message, settings.DEFAULT_FROM_EMAIL, to=[to_mail,])
    mail.send()
