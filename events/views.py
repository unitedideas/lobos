from .models import RiderProfile, Profile
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail, send_mass_mail, EmailMultiAlternatives, EmailMessage
from .models import Event
from django.http import JsonResponse, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from events.forms import (
    RegistrationForm,
    EditProfileForm,
    RiderProfileFormSet,
)
from django.template import loader
from django.template import Context
from anymail.message import attach_inline_image_file
from django.template.loader import render_to_string
import random
import string
import json
import datetime
from datetime import date


def home(request):
    events = Event.objects.all().order_by('-event_date')[0:3]
    event_name = events.values_list('event_name', flat=True)
    event_dates = events.values_list('event_date', flat=True)
    year_list = []
    event_date = []
    event_details = []
    event_location = []
    map_location = []
    description = []
    pre_entry_cost = []
    post_entry_cost = []
    escort_rider_cost = []
    entry_closes = []
    rider_limit = []
    reg_riders = []
    remaining_spots = []
    remaining_time = []

    for event in event_name:
        event_id = Event.objects.get(event_name=event).id
        reg_riders.append(RiderProfile.objects.filter(event=event_id).count())

    for date in event_dates:

        tte = int((date - datetime.date.today()).days)

        try:
            if tte == 0:
                remaining_time.append("It's Today!!!")
            elif tte < 1:
                remaining_time.append("Results to Come!")
            else:
                remaining_time.append(tte)
        except:
            remaining_time.append("TBD")

    for date in event_dates:
        year = str(date)[:4]
        year_list.append(year)

    for event in events:
        event_date.append(event.event_date)
        event_details.append(event.event_details)
        event_location.append(event.event_location)
        map_location.append(event.map_location)
        description.append(event.description)
        pre_entry_cost.append(event.pre_entry_cost)
        post_entry_cost.append(event.post_entry_cost)
        entry_closes.append(event.entry_closes)
        escort_rider_cost.append(event.escort_rider_cost)
        rider_limit.append(event.rider_limit)

    for limit, rider in zip(rider_limit, reg_riders):

        try:
            remaining_spots.append(limit - rider)
        except:
            remaining_spots.append('TBD')

    events_details = zip(event_name,  # 0
                         year_list,  # 1
                         event_date,  # 2
                         event_details,  # 3
                         event_location,  # 4
                         map_location,  # 5
                         description,  # 6
                         pre_entry_cost,  # 7
                         post_entry_cost,  # 8
                         entry_closes,  # 9
                         escort_rider_cost,  # 10
                         remaining_spots,  # 11
                         remaining_time,  # 12
                         )

    context = {'events_details': events_details}

    return render(request, 'events/home.html', context)


def login(request):
    return render(request, 'events/login.html')


# Email


def send_mail_user_reg(email, first_name, last_name, username, password):
    print(email)
    msg = EmailMultiAlternatives(
        subject="Welcome to Lobos",
        body="Click to activate your account: http://example.com/activate",
        from_email="The Lobos Team <info@lobosmc.com.com>",
        to=[email],
        reply_to=["Lobos Support <info@lobosmc.com.com>"])

    html = loader.render_to_string(
        '../templates/events/userregistertemplate.html',
        {
            'name': first_name.title() + " " + last_name.title(),
            'username': username,
            'first_name': first_name.title(),
            'last_name': last_name.title,
            'password': password,
        }
    )
    msg.attach_alternative(html, "text/html")

    # Optional Anymail extensions:
    msg.tags = ["activation", "onboarding"]
    msg.track_clicks = True

    # Send it:
    msg.send()


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():

            email = request.POST['email'].replace(" ", "")
            first_name = request.POST['first_name'].replace(" ", "")
            last_name = request.POST['last_name'].replace(" ", "")
            username = first_name.lower() + last_name.lower() + email.lower().replace(" ", "")
            password = request.POST['password1']

            if User.objects.filter(username=username).exists():
                user_id = User.objects.get(username=username).id
                form = RegistrationForm()
                args = {'form': form,
                        'errors': 'A user with that username already exists. Please choose a different one.'}
                return render(request, 'events/reg_form.html', args)

            else:
                form.save()
                send_mail_user_reg(email, first_name, last_name, username, password)
                return redirect('/login/')


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
            subject = 'LobosEvents.com Password Change'
            from_email = 'MrWolf@LobosEvents.com'
            to = request.user.email
            first_name = request.user.first_name
            username = request.user.username

            text_content = 'Hi ' + first_name.title() + '\nYou recently requested to reset your password at LobosEvents.com. \n' \
                                                        'Your username, in case you\'ve forgotten: ' + username

            html_content = 'Hi ' + first_name.title() + '\nYou recently requested to reset your password at LobosEvents.com. \n' \
                                                        'Your username, in case you\'ve forgotten: ' + username

            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return redirect('/profile/')
        else:
            errors = {'errors': formset.errors}
            return redirect('change_password', errors)
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'events/password_change.html', args)


def error_checking(request):
    print('in error checking')
    forms = json.load(request)  # The form as html string
    formset = RiderProfileFormSet(forms)
    if formset.is_valid():
        print('VALID')
        content = {'success': True}
        return JsonResponse(content)
    else:
        print('NOT VALID')
        content = {'errors': formset.errors, 'success': False}
        return JsonResponse(content)


def event_mail(email, first_name, last_name, username, rider_cat, rider_class, event, confirmation_number):
    msg = EmailMultiAlternatives(
        subject="You're Registered!",
        from_email="The Lobos Team <info@lobosmc.com.com>",
        to=[email],
        reply_to=["Lobos Support <info@lobosmc.com.com>"])

    html = loader.render_to_string(
        '../templates/events/eventregistertemplate.html',
        {
            'event': event,
            'rider_cat':rider_cat,
            'rider_class': rider_class,
            'name': first_name.title() + " " + last_name.title(),
            'username': username,
            'first_name': first_name.title(),
            'last_name': last_name.title,
            'confirmation_number': confirmation_number,
        }
    )
    msg.attach_alternative(html, "text/html")

    # Optional Anymail extensions:
    msg.tags = ["event_registration"]
    msg.track_clicks = True

    # Send it:
    msg.send()


def event_register(request):
    if request.method == 'POST':

        formset_post = RiderProfileFormSet(request.POST)

        if formset_post.is_valid():
            print('formset valid')
            formset = formset_post.save(commit=False)
            confirmation_number = id_generator()
            count = 0
            confirm = {}
            for form in formset:
                count += 1
                print('in the form loop')
                created_username = form.first_name + form.last_name + form.email
                print('form.birth_date')
                print(form.birth_date)
                print(type(form.birth_date))

                # need to calculate the age on the event date
                # age_on_event_day = form.birth_date - Event.event_date
                # print(age_on_event_day)

                form.confirmation_number = confirmation_number
                form.event = Event.objects.get(event_name=request.GET.get('event'))
                event = str(form.event)

                if User.objects.filter(username=created_username).exists():
                    user_id = User.objects.get(username=created_username).id

                if not User.objects.filter(username=created_username).exists():
                    print('The user does not exist')
                    print('Creating a new profile')
                    user = User.objects.create(username=created_username,
                                               email=form.email,
                                               first_name=form.first_name,
                                               last_name=form.last_name,
                                               )

                    user.first_name = form.first_name
                    user.last_name = form.last_name
                    user.save()
                    print('saved new user')
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

                    message = ''
                    username = created_username
                    first_name = form.first_name
                    last_name = form.last_name
                    email = form.email
                    rider_cat = form.rider_cat
                    rider_class = form.rider_class

                    confirm[created_username] = {'message': message,
                                                 'username': username,
                                                 'first_name': first_name,
                                                 'last_name': last_name,
                                                 'email': email,
                                                 'confirmation': confirmation_number,
                                                 'rider_cat': rider_cat,
                                                 'rider_class': rider_class}
                    form.save()

                    #Email
                    event_mail(email, first_name, last_name, username, rider_cat, rider_class, event,
                               confirmation_number)


                elif RiderProfile.objects.filter(event=form.event).filter(user=user_id).exists():
                    print('Already registered for this event')
                    form.user = User.objects.get(username=created_username)
                    username = created_username
                    first_name = form.first_name
                    last_name = form.last_name
                    email = form.email
                    rider_cat = form.rider_cat
                    rider_class = form.rider_class

                    # if we want to send the old confirmation number, uncomment below code
                    # confirmation = RiderProfile.objects.get(event=form.event, user=user_id).confirmation_number

                    message = 'The rider, ' + first_name + ' ' + last_name + ', has previously been registered.' + \
                              ' Please contact the person you registered to verify.' \
                              ' If they have been registered twice please contact us for a refund for that entry.' \
                              ' Email us at info@lobosmc.com'

                    confirm[created_username] = {'message': message,
                                                 'username': username,
                                                 'first_name': first_name,
                                                 'last_name': last_name,
                                                 'email': email,
                                                 'confirmation': confirmation_number,
                                                 'rider_cat': rider_cat,
                                                 'rider_class': rider_class}
                    form.save()

                    #Email
                    event_mail(email, first_name, last_name, username, rider_cat, rider_class, event,
                               confirmation_number)



                else:
                    print('The user already has a profile')
                    print('Registering this user for the event')
                    form.user = User.objects.get(username=created_username)
                    username = created_username
                    first_name = form.first_name
                    last_name = form.last_name
                    email = form.email
                    rider_cat = form.rider_cat
                    rider_class = form.rider_class

                    confirm[created_username] = {'username': username,
                                                 'first_name': first_name,
                                                 'last_name': last_name,
                                                 'email': email,
                                                 'confirmation': confirmation_number,
                                                 'rider_cat': rider_cat,
                                                 'rider_class': rider_class}

                    form.save()

                    #Email
                    event_mail(email, first_name, last_name, username, rider_cat, rider_class, event,
                               confirmation_number)


            args = {'event': form.event, 'confirm': confirm}
            # email confirmation function here
            return render(request, 'events/event_confirmation.html', args)
        else:
            print('formset not valid')
            print(formset_post.errors)
            errors = formset_post.errors
            # can start with the current users filter queryset
            # AuthorFormSet(queryset=Author.objects.filter(name__startswith='O'))

            event = Event.objects.get(event_name=request.GET.get('event'))
            formset = prefill_form(request)

            args = {'formset': formset, 'event': event, 'errors': errors}
            return render(request, 'events/event_register.html', args)

    else:

        event = Event.objects.get(event_name=request.GET.get('event'))

        formset = prefill_form(request)

        args = {'formset': formset, 'event': event}
        return render(request, 'events/event_register.html', args)


def event_confirmation(request):
    args = {'request': request, 'user': request.user}
    return render(request, 'events/event_confirmation.html', args)


def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def event_formset(request):
    formset = prefill_form(request)
    formset = str(formset)
    event = json.loads(request.body)['event'][0:-5]
    event_date = json.loads(request.body)['event'][-4:]
    escort_rider_cost = Event.objects.get(event_name=event, event_date__contains=event_date).escort_rider_cost
    reg_rider_cost = Event.objects.get(event_name=event, event_date__contains=event_date).pre_entry_cost
    # reg_rider_cost = Event.objects.get(event_name=request.GET.get('event')).pre_entry_cost
    formset_to_vue = {'reg_rider_cost': reg_rider_cost, 'escort_rider_cost': escort_rider_cost, 'formset': formset}
    return JsonResponse(formset_to_vue)


def prefill_form(request):
    form_fill_dict = {}
    profile_field_names = []
    prof = request.user.profile

    for field in Profile._meta.get_fields():
        if field.name is not 'id':
            profile_field_names.append(field.name)
            field = str(field.name)
            form_fill_dict[field] = getattr(prof, field)

    user_field_names = ['first_name', 'last_name', 'email']
    user_prof = request.user
    for field in User._meta.get_fields():
        field = str(field.name)
        if field in user_field_names:
            form_fill_dict[field] = getattr(user_prof, field)
    return RiderProfileFormSet(queryset=RiderProfile.objects.none(), initial=[form_fill_dict])
