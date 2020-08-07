from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import RiderProfile, Profile, ClubEvent, SignupPromotion
import os
from django.forms import modelformset_factory, formset_factory
from django.forms import ModelForm, NumberInput, DateInput
from events.util import load_choices
from django.forms import BaseModelFormSet
from django.core.exceptions import ValidationError

HERE = os.path.abspath(os.path.dirname(__file__))
STATES_PATH = os.path.join(HERE, 'states.txt')
STATES = load_choices(STATES_PATH, True)


class MerchandiseOrderForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'v-model': 'form.first_name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'v-model': 'form.last_name'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'v-model': 'form.address'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'v-model': 'form.city'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'v-model': 'form.state'}))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={'v-model': 'form.zip_code'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'v-model': 'form.email'}))
    items_ordered = forms.CharField(widget=forms.HiddenInput(attrs={'id': "order_data"}))


class RegistrationCheck(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name', required=False)
    last_name = forms.CharField(max_length=30, label='Last Name', required=False)
    confirmationNumber = forms.CharField(max_length=30, label='Confirmation Number', required=False)


class MyAuthenticationForm(AuthenticationForm):
    username = forms.CharField(required=False,
                               widget=forms.TextInput(attrs={'oninput': "this.value=this.value.toLowerCase()"}))


class RegistrationForm(UserCreationForm):
    FEMALE = 'Female'
    MALE = 'Male'

    GENDER = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
    )

    email = forms.EmailField()
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    gender = forms.ChoiceField(choices=GENDER, initial='Male')
    birth_date = forms.DateField(required=False,
                                 widget=forms.DateInput(attrs={"type": "date", 'placeholder': '12/14/1980'}))
    phone_number = forms.CharField(max_length=10, required=False,
                                   widget=forms.NumberInput(attrs={'placeholder': '2223334444'}))
    country = forms.CharField(required=False)
    address = forms.CharField(required=False)
    address_line_two = forms.CharField(required=False)
    city = forms.CharField(max_length=300, required=False)
    state = forms.ChoiceField(choices=STATES, initial='OR', required=False)
    zip_code = forms.CharField(max_length=5, required=False)
    emergency_contact_name = forms.CharField(max_length=300, required=False)
    emergency_contact_phone = forms.CharField(max_length=10, required=False,
                                              widget=forms.NumberInput(attrs={'placeholder': '2223334444'}))

    class Meta:
        model = User
        fields = (
            # 'username',
            'email',
            'first_name',
            'last_name',
            'gender',
            'birth_date',
            'phone_number',
            'country',
            'address',
            'address_line_two',
            'city',
            'state',
            'zip_code',
            'emergency_contact_name',
            'emergency_contact_phone',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name'].replace(" ", "")
        user.last_name = self.cleaned_data['last_name'].replace(" ", "")
        user.email = self.cleaned_data['email'].replace(" ", "")
        user.username = user.first_name + user.last_name + user.email
        user.username = user.username.replace(" ", "").lower()
        user.save()
        new_user = Profile.objects.filter(user=user)
        new_user.update(gender=self.cleaned_data['gender'])
        new_user.update(birth_date=self.cleaned_data['birth_date'])
        new_user.update(phone_number=self.cleaned_data['phone_number'])
        new_user.update(country=self.cleaned_data['country'])
        new_user.update(address=self.cleaned_data['address'])
        new_user.update(address_line_two=self.cleaned_data['address_line_two'])
        new_user.update(city=self.cleaned_data['city'])
        new_user.update(state=self.cleaned_data['state'])
        new_user.update(zip_code=self.cleaned_data['zip_code'])
        new_user.update(emergency_contact_name=self.cleaned_data['emergency_contact_name'])
        new_user.update(emergency_contact_phone=self.cleaned_data['emergency_contact_phone'])
        if commit:
            user.save()
        return user


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
        )


class LobosRace(ModelForm):
    class Meta:
        model = ClubEvent
        fields = '__all__'
        widgets = {'riderClass': forms.Select(attrs={
            'v-on:change': 'select_change()'
        })}


class RiderClass(ModelForm):
    EXO16 = 'Expert 16 and over '
    # EXU16 = 'Expert under 16 '
    # AMO16 = 'Amateur 16 and over '
    # AMU16 = 'Amateur under 16 '
    # C60_70 = 'Class 60 and 70 '
    # ES = 'Escort Rider'
    #
    # C60 = '60 Class'
    # C70 = '70 Class'
    AA = 'AA'
    # OAM = 'Open Amateur'
    # AM250 = '250 AM'
    # EX250 = '250 EX'
    # AM30 = '30 AM'
    # EX30 = '30 EX'
    # AM40 = '40 AM'
    # EXEX40 = '40 EX'
    # EX50 = '50 EX'
    # AM50 = '50 AM'
    # SSMN = 'Sportsman'
    # BEG = 'Beginner'
    # WO = 'Women'
    # JR = 'Jr.'
    # OEX = 'Open Expert'

    RIDER_CLASS = [
        (EXO16, [
            (EXO16 + AA, AA),
            # (EXO16 + OEX, OEX),
            # (EXO16 + EX250, EX250),
            # (EXO16 + EX30, EX30),
            # (EXO16 + EXEX40, EXEX40)
        ])
        # ,
        # (EXU16, [
        #     (EXU16 + AA, AA),
        #     (EXU16 + OEX, OEX),
        #     (EXU16 + EX250, EX250)
        # ]),
        # (AMO16, [
        #     (AMO16 + OAM, OAM),
        #     (AMO16 + AM250, AM250),
        #     (AMO16 + AM30, AM30),
        #     (AMO16 + AM40, AM40),
        #     (AMO16 + AM50, AM50),
        #     (AMO16 + EX50, EX50),
        #     (AMO16 + SSMN, SSMN),
        #     (AMO16 + BEG, BEG),
        #     (AMO16 + WO, WO)
        # ]),
        # (AMU16, [
        #     (AMU16 + OAM, OAM),
        #     (AMU16 + AM250, AM250),
        #     (AMU16 + SSMN, SSMN),
        #     (AMU16 + BEG, BEG),
        #     (AMU16 + WO, WO),
        #     (AMU16 + JR, JR),
        # ]),
        # (C60_70, [
        #     (C60, C60),
        #     (C70, C70)
        # ]),
        # (ES, [
        #     (ES, ES)]
        #  )
    ]

    promotion_classes = forms.MultipleChoiceField(help_text='You must choose classes every time.', choices=RIDER_CLASS,
                                                  widget=forms.SelectMultiple)

    class Meta:
        fields = '__all__'


class BaseRiderProfileFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


RiderProfileFormSet = modelformset_factory(RiderProfile,
                                           exclude=(
                                               'rider_cat', 'user', 'confirmation_number', 'start_time', 'event', 'id',
                                               'registration_date_time'),
                                           formset=BaseRiderProfileFormSet,
                                           widgets={
                                               'birth_date': DateInput(
                                                   attrs={
                                                       'v-model': 'birth_date', 'type': 'date',
                                                       'placeholder': 'Example: 12/14/1980'
                                                   }),
                                               'escort_name': forms.TextInput(
                                                   attrs={
                                                       'placeholder': 'Escort Rider Required if under 16 on the day of the event.'
                                                   }),
                                               'riding_together': forms.TextInput(
                                                   attrs={
                                                       'placeholder': 'John Smith, Jane Doe'}),
                                               'email': forms.EmailInput(
                                                   attrs={
                                                       'onpaste': 'return false', 'onCopy': 'return false',
                                                       'onCut': 'return false', 'onDrag': 'return false',
                                                       'onDrop': 'return false'
                                                   }),
                                               'email2': forms.EmailInput(
                                                   attrs={
                                                       'onpaste': 'return false', 'onCopy': 'return false',
                                                       'onCut': 'return false', 'onDrag': 'return false',
                                                       'onDrop': 'return false'
                                                   }),
                                               'rider_class': forms.Select(
                                                   attrs={
                                                       'oninput': "select_class_change(this); ",
                                                   }),
                                               'discount_code': forms.TextInput(attrs={'oninput': "discount(this); ",
                                                                                       }),
                                               'merchandise_ordered': forms.HiddenInput(),
                                               'items_ordered': forms.HiddenInput(attrs={'id': "order_data"}),
                                               'promotional_item': forms.Select(
                                                   attrs={'class': 'hide', 'oninput': "select_promo_change(this); "}),
                                               'promotion_name': forms.HiddenInput(),
                                               'promotion_options': forms.Select(attrs={'class': 'hide'}),
                                           })
