from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_approval_mail
from django.template.defaultfilters import slugify
import datetime as dt
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.utils.deconstruct import deconstructible

class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='user_profile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=128, unique=True)
    vendor_license = models.ImageField(upload_to='vendors/license')
    vendor_slug = models.SlugField(max_length=128, unique=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.id:
            previous_obj = Vendor.objects.get(id=self.id)
            if self.is_approved != previous_obj.is_approved:
                send_approval_mail(previous_obj)
            
        self.vendor_slug = slugify(self.vendor_name)
        return super(Vendor, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.vendor_name
    

DAY_CHOICES = [
    ('1', 'Monday'),
    ('2', 'Tuesday'),
    ('3', 'Wednesday'),
    ('4', 'Thursday'),
    ('5', 'Friday'),
    ('6', 'Saturday'),
    ('7', 'Sunday'),
]


def get_time_choices():
    end_time_str = '12/09/2000 12:00 AM'
    start_time_str = '11/09/2000 12:00 AM'

    end_time = dt.datetime.strptime(end_time_str, '%d/%m/%Y %I:%M %p')
    start_time = dt.datetime.strptime(start_time_str, '%d/%m/%Y %I:%M %p')

    difference = dt.timedelta(minutes=30)

    TIME_CHOICES = []
    database_values_differnece = 0.5
    current_database_value = 0.0

    while start_time < end_time:
        TIME_CHOICES.append((current_database_value ,start_time.strftime('%I:%M %p')))
        start_time += difference
        current_database_value += database_values_differnece

    return TIME_CHOICES

TIME_CHOICES = get_time_choices()


# @deconstructible
# class OpeningOverlapValidator(object):
#     day = -1
#     vendor = None

#     def __init__(self, day, vendor):
#         self.day = day
#         self.vendor = vendor

#     def __call__(self, value):
#         print(self.day)
#         open_slabs = OpeningHours.objects.filter(vendor=self.vendor, day=self.day)
#         for slab in open_slabs:
#             if value >= slab.open and value < slab.close:
#                 raise ValidationError(_('There is an overlap in the opening hour for this day'), code=500)
    
#     def __eq__(self, other):
#         return isinstance(other, self.__class__) and self.day == other.day and self.vendor == other.vendor

class OpeningHours(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.CharField(choices=DAY_CHOICES)
    open = models.FloatField(choices=TIME_CHOICES)
    close = models.FloatField(choices=TIME_CHOICES)
    is_closed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.vendor.vendor_name
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(OpeningHours, self).save(*args, **kwargs)

    def clean(self):
        open_slabs = OpeningHours.objects.filter(vendor=self.vendor, day=self.day)
       
        if self.open >= self.close:
            raise ValidationError(_('Restaurant must Open before Closing'), code=500)

        for slab in open_slabs:
            if self.open >= slab.open and self.open < slab.close:
                raise ValidationError(_('There is an overlap in the Opening hour for this day'), code=501)
    
            if self.close > slab.open and self.close <= slab.close:
                raise ValidationError(_('There is an overlap in the Closing hour for this day'), code=502)

        super(OpeningHours, self).clean()

