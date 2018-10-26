import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from events.util import load_choices

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
    entry_closes = models.CharField(max_length=800, null=True, blank=True)
    event_date = models.DateField(max_length=30, null=True, blank=True)
    event_location = models.CharField(max_length=300, null=True, blank=True)
    event_details = models.TextField(max_length=1000, null=True, blank=True)
    map_location = models.TextField(max_length=800, null=True, blank=True)
    expert_time_est = models.TimeField(max_length=30, null=True, blank=True)
    amateur_time_est = models.TimeField(max_length=30, null=True, blank=True)
    rider_limit = models.IntegerField(null=True, blank=True)
    expert_over_16_cost = models.IntegerField()
    expert_under_16_cost = models.IntegerField()
    amateur_over_16_cost = models.IntegerField()
    amateur_under_16_cost = models.IntegerField()
    class_60_and_class_70_cost = models.IntegerField()
    escort_rider_cost = models.IntegerField()
    open_registration = models.BooleanField(default=False)
    hat = models.BooleanField('Check the box if there is hat merchandise', default=False)
    hat_image_file_name = models.CharField(max_length=300, null=True, blank=True)
    hat_main_description = models.CharField(max_length=300, null=True, blank=True)
    hat_sub_description = models.CharField(max_length=300, null=True, blank=True)
    hat_cost = models.IntegerField(null=True, blank=True)
    hat_Xsmall = models.BooleanField(default=False)
    hat_small = models.BooleanField(default=False)
    hat_medium = models.BooleanField(default=False)
    hat_large = models.BooleanField(default=False)
    hat_Xlarge = models.BooleanField(default=False)
    hat_XXlarge = models.BooleanField(default=False)
    hat_XXXlarge = models.BooleanField(default=False)

    hoodie = models.BooleanField('Check the box if there is hoodie merchandise', default=False)
    hoodie_image_file_name = models.CharField(max_length=300, null=True, blank=True)
    hoodie_main_description = models.CharField(max_length=300, null=True, blank=True)
    hoodie_sub_description = models.CharField(max_length=300, null=True, blank=True)
    hoodie_cost = models.IntegerField(default=False)
    hoodie_Xsmall = models.BooleanField(default=False)
    hoodie_small = models.BooleanField(default=False)
    hoodie_medium = models.BooleanField(default=False)
    hoodie_large = models.BooleanField(default=False)
    hoodie_Xlarge = models.BooleanField(default=False)
    hoodie_XXlarge = models.BooleanField(default=False)
    hoodie_XXXlarge = models.BooleanField(default=False)

    shirt = models.BooleanField('Check the box if there is shirt merchandise', default=False)
    shirt_image_file_name = models.CharField(max_length=300, null=True, blank=True)
    shirt_main_description = models.CharField(max_length=300, null=True, blank=True)
    shirt_sub_description = models.CharField(max_length=300, null=True, blank=True)
    shirt_cost = models.IntegerField(default=False)
    shirt_Xsmall = models.BooleanField(default=False)
    shirt_small = models.BooleanField(default=False)
    shirt_medium = models.BooleanField(default=False)
    shirt_large = models.BooleanField(default=False)
    shirt_Xlarge = models.BooleanField(default=False)
    shirt_XXlarge = models.BooleanField(default=False)
    shirt_XXXlarge = models.BooleanField(default=False)

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

    def __str__(self):
        return str(self.user.first_name) + " " + str(self.user.last_name) + " - " + str(self.user)


class Codes(models.Model):
    discount_code = models.CharField(max_length=100, null=True, blank=True)
    discount_amount = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.discount_code) + " " + str(self.discount_amount)


class RiderProfile(models.Model):
    FEMALE = 'Female'
    MALE = 'Male'

    EXO16 = 'Expert over 16 '
    EXU16 = 'Expert 16 and under '
    AMO16 = 'Amateur over 16 '
    AMU16 = 'Amateur 16 and under '
    C60_70 = 'Class 60 and 70 '
    ES = 'Escort Rider'

    C60 = '60 Class'
    C70 = '70 Class'
    AA = 'AA'
    OAM = 'Open Amateur'
    AM250 = '250 AM'
    EX250 = '250 EX'
    AM30 = '30 AM'
    EX30 = '30 EX'
    AM40 = '40 AM'
    EXAM40 = '40 EX-AM'
    EXEX40 = '40 EX-EX'
    EX50 = '50 EX'
    AM50 = '50 AM'
    SSMN = 'Sportsman'
    BEG = 'Beginner'
    WO = 'Women'
    JR = 'Jr.'
    OEX = 'Open Expert'

    RIDER_CLASS = [
        (EXO16, [
            (EXO16 + AA, AA),
            (EXO16 + OEX, OEX),
            (EXO16 + EX250, EX250),
            (EXO16 + EX30, EX30),
            (EXO16 + EXEX40, EXEX40)
        ]),
        (EXU16, [
            (EXU16 + AA, AA),
            (EXU16 + OEX, OEX),
            (EXU16 + EX250, EX250)
        ]),
        (AMO16, [
            (AMO16 + OAM, OAM),
            (AMO16 + AM250, AM250),
            (AMO16 + AM30, AM30),
            (AMO16 + EXAM40, EXAM40),
            (AMO16 + AM40, AM40),
            (AMO16 + AM50, AM50),
            (AMO16 + EX50, EX50),
            (AMO16 + SSMN, SSMN),
            (AMO16 + BEG, BEG),
            (AMO16 + WO, WO)
        ]),
        (AMU16, [
            (AMU16 + OAM, OAM),
            (AMU16 + AM250, AM250),
            (AMU16 + SSMN, SSMN),
            (AMU16 + BEG, BEG),
            (AMU16 + WO, WO),
            (AMU16 + JR, JR),
        ]),
        (C60_70, [
            (C60, C60),
            (C70, C70)
        ]),
        (ES, [
            (ES, ES)]
         )]

    GENDER = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
    )
    # user name displayed at login
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    rider_cat = models.CharField('Rider Category', max_length=1000, null=True, blank=True)
    rider_class = models.CharField('Rider Class (required)', max_length=1000, choices=RIDER_CLASS)
    first_name = models.CharField('First Name (required)', max_length=300)
    last_name = models.CharField('Last Name (required)', max_length=300)
    email = models.EmailField('Email (required)', max_length=300)
    gender = models.CharField(null=True, blank=True, max_length=10, choices=GENDER)
    birth_date = models.DateField('Birth Date (required)')
    phone_number = models.CharField('Phone Number', max_length=10, null=True, blank=True)
    country = models.CharField(max_length=300, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    address_line_two = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=300, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True, choices=STATES)
    zip_code = models.CharField('Zip Code', max_length=5, null=True, blank=True)
    emergency_contact_name = models.CharField('Emergency Contact Name', max_length=300, null=True, blank=True)
    emergency_contact_phone = models.CharField('Emergency Contact Phone', max_length=10, null=True, blank=True)
    bike_make = models.CharField('Bike Manufacturer', max_length=20, choices=MAKES)
    bike_displacement = models.IntegerField('Bike Displacement', null=True, blank=True)
    escort_name = models.CharField(
        'Your Escort’s Name: (Must register only in the Escort class) Add another rider, below (required)',
        max_length=300)
    group_name = models.CharField('Riding in a group? Enter their First and Last names here:', max_length=1000,
                                  null=True, blank=True)
    merchandise_ordered = models.TextField(max_length=1000, null=True, blank=True, default=None)

    # These items will not be in the form and must not be visible
    # confirmation will be generated, age on event day will be calculated
    # rider number and start time will be assigned
    # registration_date_time is not editable with auto_now_add = true

    registration_date_time = models.DateTimeField('Created Time', editable=True, auto_now_add=True)
    age_on_event_day = models.IntegerField(null=True, blank=True, )
    confirmation_number = models.CharField(max_length=30, null=True, blank=True)
    rider_number = models.IntegerField(null=True, blank=True)
    start_time = models.TimeField(max_length=30, null=True, blank=True)

    # if we want to allow user profile images
    # https://www.youtube.com/watch?v=tT2JOpfelSg&list=PLw02n0FEB3E3VSHjyYMcFadtQORvl1Ssj&index=36

    def __str__(self):
        return str(self.event) + ' ' + str(self.user)


class Person(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(null=True, blank=True, )
    birth_date = models.DateField()
    location = models.CharField(max_length=100, blank=True)


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
