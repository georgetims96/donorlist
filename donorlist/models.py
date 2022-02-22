from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from .helpers import get_latitude, get_longitude, geocode

# Defines blood type for drop-down menu for profile creation
BLOOD_TYPES = (
    ('ab+','AB+'),
    ('ab-', 'AB-'),
    ('a-','A-'),
    ('a+','A+'),
    ('b+','B-'),
    ('b+','B+'),
    ('o-','O-'),
    ('o+','O+'),
)

# Extension of Django user with one-to-one to add additional data
class Profile(models.Model):
    # Connect User to Profile model with OneToOne
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    # Field for First Name entry
    first_name = models.CharField(null = True, max_length = 50)
    # Field for Last Name entry
    last_name = models.CharField(null = True, max_length = 50)
    # Field for City entry; !!!!! TBD - should we calculate user's coordinates at instantiation? !!!!!
    city = models.CharField(null = True, max_length = 50)
    # Field for Birthday entry
    birth_date = models.DateField(null = True, blank = True)
    # Field for Email Address entry
    email_address = models.EmailField(null = True, blank = True)
    # Field for Blood Type Entry
    blood_type = models.CharField(max_length = 3, choices = BLOOD_TYPES, default = 'ab+')
    # Field for Longitude
    longitude = models.CharField(max_length = 50, null = True, blank = True)
    # Field for Latitude
    latitude = models.CharField(max_length = 50, null = True, blank = True)

    # formatting tweak so title shows in admin for ease of viewing
    def __str__(self):
        return self.first_name
    
    # Returns all of the field names of the Profile object. This will be useful in the views.py
    @property
    def fields(self):
        return [ f.name for f in self._meta.fields + self._meta.many_to_many ]

# Try saving the profile, and if it does not exist, create it
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)
