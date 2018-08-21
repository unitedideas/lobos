from django.shortcuts import render, redirect
from events.forms import (
    RegistrationForm,
    EditProfileForm,
    RiderProfileFormSet,
)
import random
import string
from .models import RiderProfile, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import Event
from django.http import HttpResponse, JsonResponse
import json
import datetime


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


def error_checking(request):
    print('in error checking')
    # request_data = json.loads(request.body)['form_to_validate']  # The form as html string
    # Error: AttributeError: 'str' object has no attribute 'get'



    # request_data = json.load(request.POST)  # The form as a dict {'form_to_validate': '<form id="reg_form" method.....}
    #Error: ValidationError: ['ManagementForm data is missing or has been tampered with']



    # request_data = RiderProfileFormSet(request.POST)
    #Error: ValidationError: ['ManagementForm data is missing or has been tampered with']

    # request_data.clean()
    # super(request_data).clean()
    # print(request_data)




    if request.POST:
        form = RiderProfileFormSet(request.POST)
        print('made it')
        if form.is_valid():
            print('NOT')
            return JsonResponse({'success': True})
        else:
            print('YES')
            return JsonResponse({'error': form.errors})


    # if formset_post.is_valid():
    #     print('the formset is valid')
    #     print('passing to event_register')
    #     event_register(request)
    # else:
    #     print('formset not valid')
    #     print(formset_post.errors)
    #     errors = formset_post.errors
    #     args = {'errors': errors}
    #     return JsonResponse(args)


def event_register(request):
    if request.method == 'POST':

        formset_post = RiderProfileFormSet(request.POST)
        print(type(formset_post))

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
                form.confirmation_number = confirmation_number
                form.event = Event.objects.get(event_name=request.GET.get('event'))

                #
                # create username first by combining first, last and email used in the form
                #  and check if in User.obj.username.exists
                if User.objects.filter(username=created_username).exists():
                    user_id = User.objects.get(username=created_username).id

                if not User.objects.filter(username=created_username).exists():
                    print('The user does not exist')
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

                    # RiderProfile.objects.all().last().delete()
                    message = ''
                    username = created_username
                    first_name = form.first_name
                    last_name = form.last_name
                    email = form.email
                    rider_class = form.rider_class

                    confirm[created_username] = {'message': message,
                                                 'username': username,
                                                 'first_name': first_name,
                                                 'last_name': last_name,
                                                 'email': email,
                                                 'confirmation': confirmation_number,
                                                 'rider_class': rider_class}
                    form.save()

                elif RiderProfile.objects.filter(event=form.event).filter(user=user_id).exists():
                    print('Already registered for this event')
                    username = created_username
                    first_name = form.first_name
                    last_name = form.last_name
                    email = form.email
                    rider_class = form.rider_class
                    confirmation = RiderProfile.objects.get(event=form.event, user=user_id).confirmation_number
                    message = 'The rider, ' + first_name + ' ' + last_name + ', has previously been registered.' + \
                              ' Please contact the person you registered to verify.' \
                              ' If they have been registered twice please contact us for a refund for that entry.' \
                              ' Phone: 333-333-4444 or email: NotShane@Lobosevents.com'

                    confirm[created_username] = {'message': message,
                                                 'username': username,
                                                 'first_name': first_name,
                                                 'last_name': last_name,
                                                 'email': email,
                                                 'confirmation': confirmation,
                                                 'rider_class': rider_class}
                else:
                    print('The user exists')
                    form.user = User.objects.get(username=created_username)
                    username = created_username
                    first_name = form.first_name
                    last_name = form.last_name
                    email = form.email
                    rider_class = form.rider_class

                    confirm[created_username] = {'username': username,
                                                 'first_name': first_name,
                                                 'last_name': last_name,
                                                 'email': email,
                                                 'confirmation': confirmation_number,
                                                 'rider_class': rider_class}

                    form.save()

            # print(confirm)

            args = {'event': form.event, 'confirm': confirm}
            # email confirmation function here
            # return redirect('/event-confirmation')
            # return render(request, 'events/event_confirmation.html')
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
        # can start with the current users filter queryset
        # AuthorFormSet(queryset=Author.objects.filter(name__startswith='O'))
        # current_user_profile = RiderProfile.objects.get(user=request.user)
        # current_user_profile = RiderProfile.objects.all()
        # ride =request.user
        # print(RiderProfile.objects.user)
        # print(current_user_profile)
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
    # print(Event.objects.get(event_name=request.GET.get('event')))
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
