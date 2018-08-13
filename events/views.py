from django.shortcuts import render, redirect
from events.forms import (
    RegistrationForm,
    EditProfileForm,
    RiderProfileFormSet,
)
import random
import string
import datetime
import urllib.parse
from .models import RiderProfile, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import Event
from django.http import JsonResponse
import json
import stringify

def home(request):
    events = Event.objects.all().order_by('-event_date')[0:3]
    event_name = events.values_list('event_name', flat=True)
    event_dates = events.values_list('event_date', flat=True)
    year_list = []
    event_date = []
    event_details = []
    event_location = []
    map_location = []
    slogan = []
    pre_entry_cost = []
    post_entry_cost = []
    entry_closes = []

    for date in event_dates:
        year = str(date)[:4]
        year_list.append(year)

    for event in events:
        event_date.append(event.event_date)
        event_details.append(event.event_details)
        event_location.append(event.event_location)
        map_location.append(event.map_location)
        slogan.append(event.slogan)
        pre_entry_cost.append(event.pre_entry_cost)
        post_entry_cost.append(event.post_entry_cost)
        entry_closes.append(event.entry_closes)

    events_details = zip(event_name,
                         year_list,
                         event_date,
                         event_details,
                         event_location,
                         map_location,
                         slogan,
                         pre_entry_cost,
                         post_entry_cost,
                         entry_closes)

    context = {'events_details': events_details}

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
            args = {'form': form, 'errors': 'A user with that username already exists. Please choose a different one.'}
            return render(request, 'events/edit_profile.html', args)
    else:
        form = EditProfileForm(instance=request.user.profile)
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


def event_register(request):
    if request.method == 'POST':
        formset_post = RiderProfileFormSet(request.POST)

        if formset_post.is_valid():
            print('formset valid')
            formset = formset_post.save(commit=False)
            confirmation_number = id_generator()
            for form in formset:
                print('in the form loop')
                print(form.email)

                form.confirmation_number = confirmation_number
                form.event = Event.objects.get(event_name=request.GET.get('event'))
                #
                # create username first by combining first, last and email used in the form
                #  and check if in User.obj.username.exists
                if not User.objects.filter(username=form.email).exists():
                    user = User.objects.create(username=form.email,
                                               email=form.email,
                                               first_name=form.first_name,
                                               last_name=form.last_name,
                                               )

                    user.save()
                    user.first_name = form.first_name
                    user.last_name = form.last_name
                    form.user = user
                    user = Profile.objects.filter(user=user)
                    user.update(address=form.address)
                    user.update(gender=form.gender)
                    user.update(birth_date=form.birth_date)
                    user.update(phone_number=form.phone_number)
                    user.update(country=form.country)
                    user.update(address_line_two=form.address_line_two)
                    user.update(city=form.city)
                    user.update(state=form.state)
                    user.update(zip_code=form.zip_code)
                    user.update(emergency_contact_name=form.emergency_contact_name)
                    user.update(emergency_contact_phone=form.emergency_contact_phone)
                    user.update(omra_number=form.omra_number)
                    user.update(ama_number=form.ama_number)

                    # RiderProfile.objects.all().last().delete()
                    # Profile.objects.update(address=form.address)


                else:
                    print('formset not valid')
                    print(formset_post.errors)
                    form.user = User.objects.get(username=form.email)
                form.save()

            # args = {'event': formset.event, 'post_email': formset.email,
            #         'confirmation_number': confirmation_number}
            # email confirmation function here
            # return redirect('/event-confirmation')
            return render(request, 'events/event_confirmation.html')
            # return render(request, 'events/event_confirmation.html', args)
        else:
            print('formset not valid')
            print(formset_post.errors)
            # can start with the current users filter queryset
            # AuthorFormSet(queryset=Author.objects.filter(name__startswith='O'))

            event = Event.objects.get(event_name=request.GET.get('event'))
            formset = RiderProfileFormSet(queryset=RiderProfile.objects.none(), initial=[
                {
                    'first_name': request.user.first_name, 'last_name': request.user.last_name,
                    'email': request.user.email, 'address': request.user.profile.address
                }])

            args = {'formset': formset, 'event': event}
            print(formset)
            return render(request, 'events/event_register.html', args)

    else:
        # can start with the current users filter queryset
        # AuthorFormSet(queryset=Author.objects.filter(name__startswith='O'))
        # current_user_profile = RiderProfile.objects.get(user=request.user)
        # current_user_profile = RiderProfile.objects.all()
        # ride =request.user
        # print(RiderProfile.objects.user)
        # print(current_user_profile)
        event = Event.objects.get(event_name=request.GET.get('event'))
        formset = RiderProfileFormSet(queryset=RiderProfile.objects.none(), initial=[
            {
                'first_name': request.user.first_name, 'last_name': request.user.last_name,
                'email': request.user.email, 'address': request.user.profile.address
            }])

        args = {'formset': formset, 'event': event}
        return render(request, 'events/event_register.html', args)


def event_confirmation(request):
    args = {'request': request, 'user': request.user}
    return render(request, 'events/event_confirmation.html', args)


def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def event_formset(request):
    formset = RiderProfileFormSet(queryset=RiderProfile.objects.none(), initial=[
        {
            'first_name': request.user.first_name, 'last_name': request.user.last_name,
            'email': request.user.email, 'address': request.user.profile.address
        }])
    formset = str(formset)
    formset_to_vue = {'formset': formset}
    return JsonResponse(formset_to_vue)
