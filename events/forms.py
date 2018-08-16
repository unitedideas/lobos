from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import RiderProfile, Profile
import os
from django.forms import modelformset_factory
from events.util import load_choices

HERE = os.path.abspath(os.path.dirname(__file__))
STATES_PATH = os.path.join(HERE, 'states.txt')
STATES = load_choices(STATES_PATH, True)


# widgets = {
#             'name': Textarea(attrs={'cols': 80, 'rows': 20}),
#         }


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
    birth_date = forms.DateField(required=False)
    phone_number = forms.CharField(max_length=10, required=False)
    country = forms.CharField(required=False)
    address = forms.CharField(required=False)
    address_line_two = forms.CharField(required=False)
    city = forms.CharField(max_length=300, required=False)
    state = forms.ChoiceField(choices=STATES, initial='OR', required=False)
    zip_code = forms.CharField(max_length=5, required=False)
    emergency_contact_name = forms.CharField(max_length=300, required=False)
    emergency_contact_phone = forms.CharField(max_length=10, required=False)
    omra_number = forms.CharField(max_length=300, required=False)
    ama_number = forms.CharField(max_length=300, required=False)

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
            'omra_number',
            'ama_number',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        user.username = user.first_name + user.last_name + user.email
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
        new_user.update(omra_number=self.cleaned_data['omra_number'])
        new_user.update(ama_number=self.cleaned_data['ama_number'])
        if commit:
            user.save()
        return user


class EditProfileForm(UserChangeForm):
    # FEMALE = 'Female'
    # MALE = 'Male'
    #
    # GENDER = (
    #     (FEMALE, 'Female'),
    #     (MALE, 'Male'),
    # )

    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.PasswordInput

    # gender = forms.ChoiceField(choices=GENDER)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)
        # Profile.objects.update(gender=self.cleaned_data['gender'])
        # Profile.objects.update(birth_date=self.cleaned_data['birth_date'])
        # Profile.objects.update(phone_number=self.cleaned_data['phone_number'])
        # Profile.objects.update(country=self.cleaned_data['country'])
        # Profile.objects.update(address=self.cleaned_data['address'])
        # Profile.objects.update(address_line_two=self.cleaned_data['address_line_two'])
        # Profile.objects.update(city=self.cleaned_data['city'])
        # Profile.objects.update(state=self.cleaned_data['state'])
        # Profile.objects.update(zip_code=self.cleaned_data['zip_code'])
        # Profile.objects.update(emergency_contact_name=self.cleaned_data['emergency_contact_name'])
        # Profile.objects.update(emergency_contact_phone=self.cleaned_data['emergency_contact_phone'])
        # Profile.objects.update(omra_number=self.cleaned_data['omra_number'])
        # Profile.objects.update(ama_number=self.cleaned_data['ama_number'])

        if commit:
            user.save()
        return user


# https://docs.djangoproject.com/en/2.1/topics/forms/modelforms/
RiderProfileFormSet = modelformset_factory(RiderProfile,
                                           exclude=(
                                               'user',
                                               'age_on_event_day',
                                               'confirmation_number',
                                               'rider_number',
                                               'start_time',
                                               'event',
                                           ))
