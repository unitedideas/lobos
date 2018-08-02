import os
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify


# from mysite.util import load_choices
# from mysite.fields import (
#     RangeIntegerField,
#     PercentageField,
# )


#   V--->--hooks extends-->---V
# User (not seen) 1----1-> Profile -1----M-> UserEvent -1----M-> Event -1----M-> SpecialTests -M----1-> UserSpecialTests -M----1->|
#  ^----------------<-----------------------<------------------------<---------------------------<----------------------------------<-V


class Profile(models.Model):
    FEMALE = 'Female'
    MALE = 'Male'

    GENDER = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
    )
    # user name displayed at login
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    gender = models.CharField( null=True, blank=True, max_length=10, choices=GENDER)

    birth_date = models.DateField(null=True, blank=True)

    # django-phonenumber module from diaper bank app
    # or use the django built-in phonenumber
    phone_number = models.CharField(max_length=300, null=True, blank=True)
    country = models.CharField(max_length=300, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    address_line_two = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=300, null=True, blank=True)
    # make a dropdown like from the diaper bank app
    state = models.CharField(max_length=300, null=True, blank=True)
    zip_code = models.CharField(max_length=300, null=True, blank=True)

    # todo every event or keep on the user profile?
    # e_c = emergency contact
    emergency_contact_name = models.CharField(max_length=300, null=True, blank=True)

    # using phone number type=phone
    emergency_contact_contact = models.CharField(max_length=300, null=True, blank=True)

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()

    def __str__(self):
        return str(self.user) + ' Contact Info'


class Event(models.Model):
    event_name = models.CharField(max_length=300, null=True, blank=True)
    event_date = models.DateField(max_length=300, null=True, blank=True)
    pro_time_est = models.TimeField(max_length=300, null=True, blank=True)
    am_time_est = models.TimeField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.event_name) + ' ' + str(self.event_date)[0:4]


class SpecialTest(models.Model):
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE)
    special_test_num = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.event) + ' - ' + ' Lap/Special Test ' + str(self.special_test_num)


class UserEvent(models.Model):
    # These will be needed in the form
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bike_make = models.CharField(max_length=300, null=True, blank=True)
    bike_displacement = models.IntegerField(null=True, blank=True)
    omra_number = models.CharField(max_length=300, null=True, blank=True)
    ama_number = models.CharField(max_length=300, null=True, blank=True)

    # These items will not be in the form and must not be visible
    # confirmation will be generated, age on event day will be calculated
    # rider number and start time will be assigned
    age_on_event_day = models.IntegerField(null=True, blank=True)
    confirmation = models.CharField(max_length=300, null=True, blank=True)
    rider_number = models.IntegerField(null=True, blank=True)
    start_time = models.TimeField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.user) + ' - ' + str(self.event) + ' - ' + str(self.rider_number)


class UserSpecialTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    specialtest = models.ForeignKey(SpecialTest, on_delete=models.CASCADE)
    start_time = models.TimeField(max_length=300, null=True, blank=True)
    stop_time = models.TimeField(max_length=300, null=True, blank=True)
    total_time = models.FloatField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.user) + ' ' + str(self.specialtest)


class Person(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    birth_date = models.DateField()
    location = models.CharField(max_length=100, blank=True)
