from django.shortcuts import render, redirect
from events.forms import (
    RegistrationForm,
    EditProfileForm,
    RiderProfileFormSet,
)
import random
import string
import urllib.parse
from .models import RiderProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import Event


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


# old registration saving for deletion before deployment
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
                                               last_name=form.last_name)
                    user.save()
                    user.first_name = form.first_name
                    user.last_name = form.last_name

                    RiderProfile.objects.all().last().delete()
                    form.user = user
                else:
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
            formset = RiderProfileFormSet()
            args = {'formset': formset, 'event': event}
            return render(request, 'events/event_register.html', args)
    else:
        # can start with the current users filter queryset
        # AuthorFormSet(queryset=Author.objects.filter(name__startswith='O'))
        print(request.user)

        event = Event.objects.get(event_name=request.GET.get('event'))
        formset = RiderProfileFormSet(queryset=RiderProfile.objects.none())
        args = {'formset': formset, 'event': event}
        return render(request, 'events/event_register.html', args)


def event_confirmation(request):
    args = {'request': request, 'user': request.user}
    return render(request, 'events/event_confirmation.html', args)


def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
