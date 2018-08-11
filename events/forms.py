from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import RiderProfile, Profile
from django.forms import ModelForm
from django.forms import modelformset_factory
import datetime


# widgets = {
#             'name': Textarea(attrs={'cols': 80, 'rows': 20}),
#         }


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    address = forms.CharField()

    class Meta:
        model = User
        fields = (
            # 'username',
            'email',
            'first_name',
            'last_name',
            'address',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.save()
        Profile.objects.update(address=self.cleaned_data['address'])
        if commit:
            user.save()
        return user


class EditProfileForm(UserChangeForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.PasswordInput
    class Meta:
        model = Profile
        exclude = ['user']


    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)
        Profile.objects.update(gender=self.cleaned_data['gender'])
        Profile.objects.update(birth_date=self.cleaned_data['birth_date'])
        Profile.objects.update(phone_number=self.cleaned_data['phone_number'])
        Profile.objects.update(country=self.cleaned_data['country'])
        Profile.objects.update(address=self.cleaned_data['address'])
        Profile.objects.update(address_line_two=self.cleaned_data['address_line_two'])
        Profile.objects.update(city=self.cleaned_data['city'])
        Profile.objects.update(state=self.cleaned_data['state'])
        Profile.objects.update(zip_code=self.cleaned_data['zip_code'])
        Profile.objects.update(emergency_contact_name=self.cleaned_data['emergency_contact_name'])
        Profile.objects.update(emergency_contact_phone=self.cleaned_data['emergency_contact_phone'])
        Profile.objects.update(omra_number=self.cleaned_data['omra_number'])
        Profile.objects.update(ama_number=self.cleaned_data['ama_number'])

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
