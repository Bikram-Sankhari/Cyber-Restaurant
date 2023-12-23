from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_approval_mail


class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='user_profile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=128)
    vendor_license = models.ImageField(upload_to='vendors/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.id:
            previous_obj = Vendor.objects.get(id=self.id)
            if self.is_approved != previous_obj.is_approved:
                send_approval_mail(previous_obj)
                
        return super(Vendor, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.vendor_name
