from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import RiderProfile
from django.forms import ModelForm
from django.forms import modelformset_factory
import datetime


# widgets = {
#             'name': Textarea(attrs={'cols': 80, 'rows': 20}),
#         }


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            # 'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password'
        )



# https://docs.djangoproject.com/en/2.1/topics/forms/modelforms/
RiderProfileFormSet = modelformset_factory(RiderProfile,
                                           exclude=(
                                                    'user',
                                                    'age_on_event_day',
                                                    'confirmation_number',
                                                    'rider_number',
                                                    'start_time',
                                                    'event',
                                                    ), extra=2)


