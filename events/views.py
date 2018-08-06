from django.shortcuts import render, redirect
from events.forms import (
    RegistrationForm,
    EditProfileForm,
    RiderEventForm,
    RiderProfileModelFormset,
)
import random
import string
from .models import RiderProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.forms import modelformset_factory


def home(request):
    name = "Name Here"
    numbers = {1, 2, 3, 4, 5}
    context = {'name': name, 'numbers': numbers}

    return render(request, 'events/home.html', context)


def login(request):
    return render(request, 'events/login.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'events/reg_form.html', args)


def profile(request):
    args = {'user': request.user}
    return render(request, 'events/profile.html', args)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/profile')

    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'events/edit_profile.html', args)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/profile')
        else:
            return redirect('change_password')

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'events/password_change.html', args)


# def event_register(request):
#     if request.method == 'POST':
#         event_form = RiderEventForm(request.POST)
#
#         if event_form.is_valid():
#             event_post = event_form.save(commit=False)
#             confirmation_number = id_generator()
#             event_post.confirmation_number = confirmation_number
#             event_post = event_form.save()
#             # print(event_post.user)
#             user = User.objects.get_or_create(username=event_post.email,
#                                               email=event_post.email,
#                                               first_name=event_post.first_name,
#                                               last_name=event_post.last_name)[0]
#             user.save()
#             user.first_name = event_post.first_name
#             user.last_name = event_post.last_name
#
#             RiderProfile.objects.all().last().delete()
#             event_post.user = user
#             event_post = event_form.save()
#
#             args = {'event': event_post.event, 'post_email': event_post.email,
#                     'confirmation_number': confirmation_number}
#             # email confirmation function here
#             # return redirect('/event-confirmation')
#             return render(request, 'events/event_confirmation.html', args)
#
#         else:
#             event_form = RiderEventForm()
#             args = {'event_form': event_form}
#             return render(request, 'events/event_register.html', args)
#     else:
#         event_form = RiderEventForm()
#         args = {'event_form': event_form}
#         return render(request, 'events/event_register.html', args)
#
#

def event_register(request):
    RiderProfileFormSet = modelformset_factory(RiderProfile, exclude=('Registration_date_time',
                                                                      'user',
                                                                      'age_on_event_day',
                                                                      'confirmation_number',
                                                                      'rider_number',
                                                                      'start_time'))
    if request.method == 'POST':
        formset_post = RiderProfileFormSet(request.POST, request.FILES)
        if formset_post.is_valid():
            formset = formset_post.save(commit=False)
            formset.email = 'sdfasdf@gmail.com'

            # confirmation_number = id_generator()
            # formset.confirmation_number = confirmation_number
            # formset.save()
            # print(formset.user)
            #
            # user = User.objects.get_or_create(username=formset.email,
            #                                   email=formset.email,
            #                                   first_name=formset.first_name,
            #                                   last_name=formset.last_name)[0]
            # user.save()
            # user.first_name = formset.first_name
            # user.last_name = formset.last_name
            #
            # RiderProfile.objects.all().last().delete()
            # formset.user = user
            # formset.save()

            # args = {'event': formset.event, 'post_email': formset.email,
            #         'confirmation_number': confirmation_number}
            # email confirmation function here
            return redirect('/event-confirmation')
            # return render(request, 'events/event_confirmation.html')
            # return render(request, 'events/event_confirmation.html', args)
        else:
            formset = RiderProfileFormSet()
            args = {'formset': formset}
            return render(request, 'events/event_register.html', args)
    else:
        # can start with the current users filter queryset
        # AuthorFormSet(queryset=Author.objects.filter(name__startswith='O'))
        formset = RiderProfileFormSet(queryset=RiderProfile.objects.none())
        args = {'formset': formset}
        return render(request, 'events/event_register.html', args)


def create_normal(request):
    template_name = 'events/create_normal.html'
    heading_message = 'Model Formset Demo'
    if request.method == 'GET':
        # we don't want to display the already saved model instances
        formset = RiderProfileModelFormset(queryset=RiderProfile.objects.all())
    elif request.method == 'POST':
        formset = RiderProfileModelFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                # only save if email is present
                if form.cleaned_data.get('email'):
                    form.save()
            return render(request, 'events/event_confirmation.html')
    return render(request, template_name, {
        'formset': formset,
        'heading': heading_message,
    })


def event_confirmation(request):
    args = {'request': request, 'user': request.user}
    return render(request, 'events/event_confirmation.html', args)


def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
