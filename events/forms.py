from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import RiderProfile
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _


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
        labels = {
            'email': _('Labels !! << this is the one'),
        }
        help_texts = {
            'email': _('help text'),
        }
        error_messages = {
            'email': {
                'max_length': _("error 1"),
            },
        }

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
            'email',
            'first_name',
            'last_name',
            'password'
        )


class RiderEventForm(ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    class Meta:
        model = RiderProfile
        exclude = [
            'Registration_date_time',
            'user',
            'age_on_event_day',
            'confirmation_number',
            'rider_number',
            'start_time'
        ]
