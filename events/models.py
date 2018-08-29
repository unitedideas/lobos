import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from events.util import load_choices
from datetime import datetime
from django.core.mail import send_mail

HERE = os.path.abspath(os.path.dirname(__file__))
STATES_PATH = os.path.join(HERE, 'states.txt')
STATES = load_choices(STATES_PATH, True)
MAKES_PATH = os.path.join(HERE, 'makes.txt')
MAKES = load_choices(MAKES_PATH, True)


class Event(models.Model):
    event_name = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    pre_entry_cost = models.IntegerField()
    post_entry_cost = models.IntegerField()
    escort_rider_cost = models.IntegerField()
    entry_closes = models.CharField(max_length=800, null=True, blank=True)
    event_date = models.DateField(max_length=30, null=True, blank=True)
    event_location = models.CharField(max_length=300, null=True, blank=True)
    event_details = models.TextField(max_length=1000, null=True, blank=True)
    map_location = models.CharField(max_length=800, null=True, blank=True)
    pro_time_est = models.TimeField(max_length=30, null=True, blank=True)
    am_time_est = models.TimeField(max_length=30, null=True, blank=True)
    rider_limit = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.event_name) + ' ' + str(self.event_date)[0:4]


class Profile(models.Model):
    FEMALE = 'Female'
    MALE = 'Male'

    GENDER = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
    )
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    gender = models.CharField(null=True, blank=True, max_length=10, choices=GENDER)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=300, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    address_line_two = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=300, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True, choices=STATES)
    zip_code = models.CharField(max_length=5, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=300, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=10, null=True, blank=True)
    omra_number = models.CharField(max_length=300, null=True, blank=True, )
    ama_number = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.user.first_name) + " " + str(self.user.last_name) + " - " + str(self.user)


class RiderProfile(models.Model):
    EXOVER16 = 'Expert Schedule Classes - Over age 16'
    EXUNDER16 = 'Expert Schedule Classes - 16 and under'
    AMOVER16 = 'Amateur Schedule Classes - Over age 16'
    AMUNDER16 = 'Expert Schedule Classes - 16 and under'
    CLASS60_70 = 'Class 60 and 70 Rider'
    ESCORT = 'Escort Rider'

    RIDER_CLASS = (
        (EXOVER16, 'Expert Schedule Classes - Over age 16'),
        (EXUNDER16, 'Expert Schedule Classes - 16 and under'),
        (AMOVER16, 'Amateur Schedule Classes - Over age 16'),
        (AMUNDER16, 'Expert Schedule Classes - 16 and under'),
        (CLASS60_70, 'Class 60 and 70 Rider'),
        (ESCORT, 'Escort Rider'),
    )

    FEMALE = 'Female'
    MALE = 'Male'

    GENDER = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
    )
    # user name displayed at login
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    rider_class = models.CharField(max_length=100, choices=RIDER_CLASS)
    first_name = models.CharField(max_length=300, null=True, blank=True)
    last_name = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField(max_length=300, null=True, blank=True)
    gender = models.CharField(null=True, blank=True, max_length=10, choices=GENDER)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=300, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    address_line_two = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=300, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True, choices=STATES)
    zip_code = models.CharField(max_length=5, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=300, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=10, null=True, blank=True)
    bike_make = models.CharField(max_length=20, null=True, blank=True, choices=MAKES)
    bike_displacement = models.IntegerField(null=True, blank=True)
    omra_number = models.CharField(max_length=300, null=True, blank=True,)
    ama_number = models.CharField(max_length=300, null=True, blank=True)

    # These items will not be in the form and must not be visible
    # confirmation will be generated, age on event day will be calculated
    # rider number and start time will be assigned
    # registration_date_time is not editable with auto_now_add = true

    registration_date_time = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    age_on_event_day = models.IntegerField(null=True, blank=True,)
    confirmation_number = models.CharField(max_length=30, null=True, blank=True)
    rider_number = models.IntegerField(null=True, blank=True)
    start_time = models.TimeField(max_length=30, null=True, blank=True)

    # if we want to allow user profile images
    # https://www.youtube.com/watch?v=tT2JOpfelSg&list=PLw02n0FEB3E3VSHjyYMcFadtQORvl1Ssj&index=36

    def __str__(self):
        return str(self.event) + ' ' + str(self.user)


class Person(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(null=True, blank=True,)
    birth_date = models.DateField()
    location = models.CharField(max_length=100, blank=True)


class Mail(models.Model):
    pass

    class Meta:
        verbose_name = "Email User"
        verbose_name_plural = "Email Users"


class MailText(models.Model):
    subject = models.CharField(max_length=800)
    message = models.TextField()
    attachment = models.FileField(null=True, blank=True,)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    send_it = models.BooleanField(default=False)  # check it if you want to send your email

    def save(self):
        if self.send_it:
            # First you create your list of users
            user_list = []
            print('after user list')

            for u in self.user:
                print('in the first form')
                user_list.append(u.email)

            # Then you can send the message.
            send_mail(str(self.subject),
                      str(self.message),
                      'from@example.com',
                      user_list,
                      fail_silently=False)

    class Meta:
        verbose_name = "Emails to send"
        verbose_name_plural = "Emails to send"




def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)

