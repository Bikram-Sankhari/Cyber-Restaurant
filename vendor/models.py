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

class OpeningHours(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.CharField(choices=DAY_CHOICES)
    open = models.FloatField(choices=TIME_CHOICES)
    close = models.FloatField(choices=TIME_CHOICES)
    is_closed = models.BooleanField(default=False)

    def get_day(self):
        return self.get_day_display()
    
    def get_open(self):
        return self.get_open_display()
    
    def get_close(self):
        return self.get_close_display()

    def __str__(self) -> str:
        return self.vendor.vendor_name
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(OpeningHours, self).save(*args, **kwargs)

    def clean(self):
        opening_overlap_entry = OpeningHours.objects.filter(vendor=self.vendor, day=self.day, open__lte = self.open, close__gte=self.open)
        closing_overlap_entry = OpeningHours.objects.filter(vendor=self.vendor, day=self.day, open__lte = self.close, close__gte=self.close)
        subset_entry = OpeningHours.objects.filter(vendor=self.vendor, day=self.day, open__gte = self.open, close__lte=self.close)

        if self.open >= self.close:
            raise ValidationError(_('Restaurant must Open before Closing'), code=500)

        if opening_overlap_entry and opening_overlap_entry[0] != self:
            raise ValidationError(_('There is an overlap in the Opening hour for this day'), code=501)

        if closing_overlap_entry and closing_overlap_entry[0] != self:
            raise ValidationError(_('There is an overlap in the Closing hour for this day'), code=502)
        
        if subset_entry and subset_entry[0] != self:
            raise ValidationError(_('There is a subset of the Open Period for this day'), code=503)

        super(OpeningHours, self).clean()

