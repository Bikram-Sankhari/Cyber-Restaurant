from django.dispatch import receiver
from .utils import payment_done_singal
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from marketplace.models import Cart

from_email = settings.DEFAULT_FROM_EMAIL


def send_order_confirmation_to_customer(sender, **kwargs):
    request = kwargs['request']
    order = kwargs['order']
    current_site = get_current_site(request)
    mail_subject = 'Order Confirmed..........'
    items = Cart.objects.filter(order=order)

    context = {
        'name': request.user.first_name,
        'items': items,
        'order': order,
        'domain': current_site,
    }

    message = render_to_string(
        'emails/order_confirmation_to_customer.html', context)
    target_email = order.user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[target_email,])
    mail.content_subtype = 'html'
    mail.send()


def send_order_confirmation_to_vendors(sender, **kwargs):
    request = kwargs['request']
    order = kwargs['order']
    current_site = get_current_site(request)
    mail_subject = 'You have a New Order !!'
    vendors = order.get_all_vendors()

    for vendor in vendors:
        items = Cart.objects.filter(
            order=order, food_item__vendor=vendor, order_status='Ordered')
        target_email = vendor.user.email
        print(items, order, vendor)
        context = {
            'vendor': vendor,
            'items': items,
            'order': order,
            'domain': current_site,
        }

        message = render_to_string('emails/order_confirmation_to_vendor.html', context)
        mail = EmailMessage(mail_subject, message,from_email, to=[target_email, ])
        mail.content_subtype = 'html'
        mail.send()
