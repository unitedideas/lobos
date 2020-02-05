import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from events.util import load_choices
from django.core.validators import MaxValueValidator, MinValueValidator

HERE = os.path.abspath(os.path.dirname(__file__))
STATES_PATH = os.path.join(HERE, 'states.txt')
STATES = load_choices(STATES_PATH, True)
MAKES_PATH = os.path.join(HERE, 'makes.txt')
MAKES = load_choices(MAKES_PATH, True)

AA = 'AA'
openExpert = 'Open Ex'
Ex250 = '250 Ex'
Ex30 = '30 Ex'
Ex40 = '40 Ex'
OpenAm = 'Open Am'
Open250 = '250 Am'
Am30 = '30 Am'
Am40 = '40 Am'

LONGCOURSE = ('Long Course - $60',
              [(openExpert, 'Open Ex'),
               (Ex250, '250 Ex'),
               (Ex30, '30 Ex'),
               (Ex40, '40 Ex'),
               (OpenAm, 'Open Am'),
               (Open250, '250 Am'),
               (Am30, '30 Am'),
               (Am40, '40 Am')])

Beginner = 'Beginner'
Women = 'Women'
Jr = 'Jr 12 - 15 yrs'
Am50 = '50 Am'
Ex50 = '50 Ex'
Over60 = '60+'

SHORTCOURSE = ('Short Course - $45',
               [(Beginner, 'Beginner'),
                (Women, 'Women'),
                (Jr, 'Jr 12 - 15 yrs'),
                (Am50, '50 Am'),
                (Ex50, '50 Ex'),
                (Over60, '60+')])

rider_classes = [SHORTCOURSE, LONGCOURSE]


class ClubEvent(models.Model):
    name = models.CharField('First and Last Name', max_length=30, null=True, blank=True)
    age = models.CharField(max_length=3, null=True, blank=True)
    address = models.CharField(max_length=60, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    zip = models.CharField(max_length=5, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=60, null=True, blank=True)
    emergencyContact = models.CharField('Emergency Contact', max_length=60, null=True, blank=True)
    bikeMakeAndCC = models.CharField('Bike Make and CC', max_length=60, null=True, blank=True)
    riderClass = models.CharField('Rider Class (Short Course - $45, Long Course - $60)', max_length=60, null=True,
                                  blank=True, choices=rider_classes)
    riderGroup = models.CharField('Group You would like to ride with (2 names)', max_length=60, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class MerchandiseOrder(models.Model):
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    zip_code = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=30, null=True, blank=True)
    paypal_order_id = models.CharField(max_length=30, null=True, blank=True)
    items_ordered = models.TextField(null=True, blank=True)
    date_ordered = models.CharField(max_length=30, null=True, blank=True)
    date_shipped = models.CharField(max_length=30, null=True, blank=True)
    shipped = models.BooleanField(default=False)

    def __str__(self):
        return str(self.first_name) + str(self.last_name)


class Merchandise(models.Model):
    available_on_merch_page = models.BooleanField(
        'On Merch Page', default=False)
    merchandise_name = models.CharField(
        max_length=300, null=True, blank=True, default='Merchandise Name')
    description = models.TextField(
        max_length=1000, null=True, blank=True, default='Merchandise Description')
    sale_price = models.FloatField(default=60.00)
    item_image = models.CharField(max_length=300, null=True, blank=True)
    one_size_fits_all_quantity_available = models.PositiveIntegerField(default=0)
    x_small_quantity_available = models.PositiveIntegerField(default=0)
    small_quantity_available = models.PositiveIntegerField(default=0)
    medium_quantity_available = models.PositiveIntegerField(default=0)
    large_quantity_available = models.PositiveIntegerField(default=0)
    x_large_quantity_available = models.PositiveIntegerField(default=0)
    xx_large_quantity_available = models.PositiveIntegerField(default=0)
    xxx_large_quantity_available = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.merchandise_name) + " $" + str(self.sale_price)


class SignupPromotion(models.Model):
    promotion_item_name = models.CharField(default='Promo title', max_length=200)
    promotion_description = models.CharField(default='Promo details', max_length=800)
    promotion_limit = models.PositiveIntegerField(default=1)
    promotion_classes = models.CharField(help_text='You must choose classes every time.', max_length=1000, null=True,
                                         blank=True)
    promotion_options = models.CharField('Promotion Options:',
                                         help_text='Please separate by commas ex.(9:00am,1:00pm,5:00pm)',
                                         max_length=1000, default='Option 1,Option 2')

    def __str__(self):
        return str(self.promotion_item_name)


class Event(models.Model):
    event_name = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    pre_entry_cost = models.PositiveIntegerField(default=0)
    post_entry_cost = models.PositiveIntegerField(default=0)
    entry_closes = models.CharField(max_length=800, null=True, blank=True)
    event_date = models.DateField(max_length=30, null=True, blank=True)
    event_location = models.CharField(max_length=300, null=True, blank=True)
    event_details = models.TextField(max_length=1000, null=True, blank=True)
    map_location = models.TextField(max_length=800, null=True, blank=True)
    expert_time_est = models.TimeField(max_length=30, null=True, blank=True)
    amateur_time_est = models.TimeField(max_length=30, null=True, blank=True)
    rider_limit = models.PositiveIntegerField(default=0)
    expert_over_16_cost = models.PositiveIntegerField(default=0)
    expert_under_16_cost = models.PositiveIntegerField(default=0)
    amateur_over_16_cost = models.PositiveIntegerField(default=0)
    amateur_under_16_cost = models.PositiveIntegerField(default=0)
    class_60_and_class_70_cost = models.PositiveIntegerField(default=0)
    escort_rider_cost = models.PositiveIntegerField(default=0)
    open_registration = models.BooleanField(default=False)
    promotion = models.ForeignKey(SignupPromotion, help_text='Leave blank if there is no promotion', null=True,
                                  blank=True, on_delete=models.SET_NULL)
    hoodie = models.BooleanField(
        'Check if up-selling hoodies after registration', default=False)
    hoodie_image_file_name = models.CharField(
        max_length=300, null=True, blank=True)
    hoodie_main_description = models.CharField(
        max_length=300, null=True, blank=True)
    hoodie_cost = models.PositiveIntegerField(null=True, blank=True, default=60)
    hoodie_Xsmall = models.BooleanField(default=False)
    hoodie_small = models.BooleanField(default=False)
    hoodie_medium = models.BooleanField(default=False)
    hoodie_large = models.BooleanField(default=False)
    hoodie_Xlarge = models.BooleanField(default=False)
    hoodie_XXlarge = models.BooleanField(default=False)
    hoodie_XXXlarge = models.BooleanField(default=False)
    hat = models.BooleanField(
        'Check if up-selling hats after registration', default=False)
    hat_image_file_name = models.CharField(
        max_length=300, null=True, blank=True)
    hat_main_description = models.CharField(
        max_length=300, null=True, blank=True)
    hat_cost = models.PositiveIntegerField(null=True, blank=True, default=60)
    hat_osfa = models.BooleanField(default=False)
    shirt = models.BooleanField(
        'Check if up-selling shirts after registration', default=False)
    shirt_image_file_name = models.CharField(
        max_length=300, null=True, blank=True)
    shirt_main_description = models.CharField(
        max_length=300, null=True, blank=True)
    shirt_cost = models.PositiveIntegerField(null=True, blank=True, default=60)
    shirt_Xsmall = models.BooleanField(default=False)
    shirt_small = models.BooleanField(default=False)
    shirt_medium = models.BooleanField(default=False)
    shirt_large = models.BooleanField(default=False)
    shirt_Xlarge = models.BooleanField(default=False)
    shirt_XXlarge = models.BooleanField(default=False)
    shirt_XXXlarge = models.BooleanField(default=False)

    def __str__(self):
        return str(self.event_name)


class Profile(models.Model):
    FEMALE = 'Female'
    MALE = 'Male'

    GENDER = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
    )
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    gender = models.CharField(null=True, blank=True,
                              max_length=10, choices=GENDER)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=300, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    address_line_two = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=300, null=True, blank=True)
    state = models.CharField(max_length=2, null=True,
                             blank=True, choices=STATES)
    zip_code = models.CharField(max_length=5, null=True, blank=True)
    emergency_contact_name = models.CharField(
        max_length=300, null=True, blank=True)
    emergency_contact_phone = models.CharField(
        max_length=10, null=True, blank=True)

    def __str__(self):
        # return str(self.user.first_name) + " " + str(self.user.last_name) + " - " + str(self.user)
        return (self.user)


class Codes(models.Model):
    discount_code = models.CharField(max_length=100, null=True, blank=True)
    discount_amount = models.FloatField(null=True, blank=True,
                                        validators=[MinValueValidator(0.05), MaxValueValidator(1)])

    def __str__(self):
        return str(self.discount_code) + " " + str(self.discount_amount)


class RiderProfile(models.Model):
    FEMALE = 'Female'
    MALE = 'Male'

    EXO16 = 'Expert 16 and over '
    EXU16 = 'Expert under 16 '
    AMO16 = 'Amateur 16 and over '
    AMU16 = 'Amateur under 16 '
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
    EXEX40 = '40 EX'
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

    YESNO = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    # user name displayed at login
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField('First Name (required)', max_length=300)
    last_name = models.CharField('Last Name (required)', max_length=300)
    rider_class = models.CharField('Rider Class (required)', max_length=1000, choices=RIDER_CLASS)
    email = models.EmailField('Email (required)', max_length=300)
    email2 = models.EmailField('Verify Email', max_length=300, null=True, blank=True)
    gender = models.CharField(null=True, blank=True, max_length=10, choices=GENDER)
    birth_date = models.DateField('Birth Date - Example: 12/14/1980 (required)')
    # age = models.IntegerField
    phone_number = models.CharField('Phone Number (required)', max_length=10)
    country = models.CharField(max_length=300, null=True, blank=True)
    address = models.CharField('Address (required)', max_length=300)
    address_line_two = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField('City (required)', max_length=300)
    state = models.CharField('State (required)', max_length=2,  choices=STATES)
    zip_code = models.CharField('Zip Code (required)', max_length=5)
    emergency_contact_name = models.CharField('Emergency Contact Name', max_length=300, null=True, blank=True)
    emergency_contact_phone = models.CharField('Emergency Contact Phone', max_length=10, null=True, blank=True)
    mach = models.CharField('Bike Manufacturer (required)', max_length=20, choices=MAKES)
    bike_displacement = models.CharField('Bike Displacement', max_length=10, null=True, blank=True)
    escort_name = models.CharField(
        'Escort’s Name: (Must register as Escort Rider) Required for riders under 16 on the day of the event',
        max_length=300, null=True, blank=True)
    riding_together = models.CharField('Riding in a group? Enter their First and Last names here:', max_length=1000,
                                       null=True, blank=True)
    merchandise_ordered = models.TextField(max_length=1000, null=True, blank=True, default=None)
    registration_date_time = models.DateTimeField('Created Time', editable=True, null=True, blank=True,
                                                  auto_now_add=True)
    promotional_item = models.CharField('Would you like to register for the Radius Offroad Riding Clinic?',
                                        max_length=3, default=YESNO[1][1],
                                        choices=YESNO)
    promotion_name = models.CharField('Promotion', max_length=300, null=True, blank=True)
    promotion_options = models.CharField('Choose your riding clinic time:', max_length=300, null=True, blank=True)

    confirmation_number = models.CharField(max_length=30, null=True, blank=True)
    discount_code = models.CharField(max_length=100, null=True, blank=True)
    items_ordered = models.TextField(null=True, blank=True)

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
