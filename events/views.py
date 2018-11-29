from .models import RiderProfile, Profile, Codes
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail, send_mass_mail, EmailMultiAlternatives, EmailMessage
from .models import Event
from django.http import JsonResponse, HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from events.forms import (
    RegistrationForm,
    EditProfileForm,
    RiderProfileFormSet,
)
from django.forms.utils import ErrorDict, ErrorList
from django.template import loader
from django.template import Context
from anymail.message import attach_inline_image_file
from django.template.loader import render_to_string
import random, string, json
from datetime import datetime as ddt
import datetime as dt


@staff_member_required
def adminemail(request):
    events = list(Event.objects.all())
    allEmails = list(User.objects.values_list("email", flat=True))
    args = {'allEmails': allEmails, 'events': events}
    if request.method == 'POST':
        data = request.POST
        subject = request.POST.get("subject")
        header = request.POST.get("header")
        subheader = request.POST.get("subheader")
        emailmessage = request.POST.get("message").replace('\n', '<br>')
        recipients = request.POST.get("recipients")

        if recipients == 'All Persons in the Database':
            recipients = allEmails
        elif "@" not in recipients:
            # getting the emails for the selected event
            event_name = recipients[:-5]
            event_year = recipients[-4:]
            # Event.objects.filter(event_name=event_name).filter(event_date__contains=event_year):
            #     print('in the for loop')
            recipients = list(
                Event.objects.filter(event_name=event_name).filter(event_date__contains=event_year).values_list(
                    'riderprofile__email', flat=True))
        else:
            recipients = list(recipients)
        args = {'allEmails': allEmails, 'events': events,
                "success": "<h3 class='bg-success'>Your email was successfully sent!</h3>"}

        general_email(subject, header, subheader, emailmessage, recipients)

        return render(request, 'events/adminemail.html', args)
    else:
        events = list(Event.objects.all())
        allEmails = list(RiderProfile.objects.values_list("email", flat=True))
        args = {'allEmails': allEmails, 'events': events}
        return render(request, 'events/adminemail.html', args)


def general_email(subject, header, subheader, emailmessage, recipients):
    msg = EmailMultiAlternatives(
        subject=subject,
        from_email="The Lobos Team <info@lobosmc.com>",
        to=recipients,
        reply_to=["Lobos Support <info@lobosmc.com>"],
    )
    msg.merge_data = {}
    msg.merge_global_data = {}

    html = loader.render_to_string(
        '../templates/events/generalemail.html',
        {
            'header': header,
            'subheader': subheader,
            'message': emailmessage,

        }
    )
    msg.attach_alternative(html, "text/html")

    # Optional Anymail extensions:
    msg.tags = ["general communication"]
    msg.track_clicks = True

    # Send it:
    msg.send()


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
    open_registration = []

    for event in event_name:
        event_id = Event.objects.get(event_name=event).id
        reg_riders.append(RiderProfile.objects.filter(event=event_id).count())

    for date in event_dates:

        tte = int((date - dt.date.today()).days)

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
        open_registration.append(event.open_registration)

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
                         open_registration,  # 13
                         )

    context = {'events_details': events_details}

    return render(request, 'events/home.html', context)


def login(request):
    return render(request, 'events/login.html')


# Email

def send_mail_user_reg(email, first_name, last_name, username, password):
    msg = EmailMultiAlternatives(
        subject="Welcome to Lobos",
        from_email="The Lobos Team <info@lobosmc.com>",
        to=[email],
        reply_to=["Lobos Support <info@lobosmc.com>"])

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
                args = {'form': form,
                        'uniqueNameErrors': '<h4>A user with this first and last name and email already exists. '
                                            '<a href="/password-reset/">Reset your password here.</a></h4>'}
                return render(request, 'events/reg_form.html', args)

            else:
                form.save()
                send_mail_user_reg(email, first_name, last_name, username, password)
                return redirect('/login/')

        else:
            args = {'form': form, 'errors': form.errors}
            return render(request, 'events/reg_form.html', args)


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
    print('In error and escort checking')
    under_16 = 0
    escorts_signed_up = 0
    over_16 = False
    forms = json.load(request)  # The form as html string
    event_date = forms["event_date"].replace(",", "")
    event_date = ddt.strptime(event_date, '%B %d %Y')
    event_date = ddt.date(event_date)

    formset = RiderProfileFormSet(forms)
    if formset.is_valid():
        # calc age
        for form in formset:
            y = 0
            m = 0
            d = 0
            birth_date = form.cleaned_data['birth_date']

            y = event_date.year - birth_date.year
            m = event_date.month - birth_date.month
            d = event_date.day - birth_date.day

            if y < 16:
                under_16 += 1
            elif y == 16 and m < 0:
                under_16 += 1
            elif y == 16 and m < 0 and d < 0:
                under_16 += 1
            else:
                over_16 = True


            if form.cleaned_data['rider_class'] == "Escort Rider" and over_16 == True:
                escorts_signed_up += 1

        if (under_16 - escorts_signed_up > 0):
            print('ESCORT NOT GOOD')
            error = 'escorts' if (under_16 - escorts_signed_up > 1) else 'escort'
            content = {'escorts_signed_up': escorts_signed_up, 'under_16': under_16, }
            return JsonResponse(content)

        else:
            print('FORM VALID & ESCORTS GOOD')
            content = {'success': True}
            return JsonResponse(content)

    else:
        print('FORM NOT VALID')
        content = {'errors': formset.errors, 'success': False, 'escorts_signed_up': escorts_signed_up,
                   'under_16': under_16, }
        return JsonResponse(content)


def event_mail(email, first_name, last_name, username, rider_class, event, confirmation_number):
    msg = EmailMultiAlternatives(
        subject="You're Registered!",
        from_email="The Lobos Team <info@lobosmc.com>",
        to=[email],
        reply_to=["Lobos Support <info@lobosmc.com>"])

    html = loader.render_to_string(
        '../templates/events/eventregistertemplate.html',
        {
            'event': event,
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
            formset = formset_post.save(commit=False)
            confirmation_number = id_generator()
            count = 0
            confirm = {}
            for form in formset:
                count += 1
                created_username = form.first_name + form.last_name + form.email
                created_username = created_username.replace(" ", "").lower()
                form.confirmation_number = confirmation_number
                form.event = Event.objects.get(event_name=request.GET.get('event'))
                event = str(form.event)

                if User.objects.filter(username=created_username).exists():
                    user_id = User.objects.get(username=created_username).id

                if not User.objects.filter(username=created_username).exists():
                    user = User.objects.create(username=created_username,
                                               email=form.email,
                                               first_name=form.first_name,
                                               last_name=form.last_name,
                                               )

                    user.first_name = form.first_name
                    user.last_name = form.last_name
                    user.save()
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

                    # Email
                    event_mail(email, first_name, last_name, username, rider_class, event,
                               confirmation_number)


                elif RiderProfile.objects.filter(event=form.event).filter(user=user_id).exists():
                    form.user = User.objects.get(username=created_username)
                    username = created_username
                    first_name = form.first_name
                    last_name = form.last_name
                    email = form.email
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
                                                 'rider_class': rider_class}
                    form.save()

                    # Email
                    event_mail(email, first_name, last_name, username, rider_class, event,
                               confirmation_number)



                else:
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

                    # Email
                    event_mail(email, first_name, last_name, username, rider_class, event,
                               confirmation_number)

            args = {'event': form.event, 'confirm': confirm}
            # email confirmation function here
            return render(request, 'events/event_confirmation.html', args)
        else:
            errors = formset_post.errors
            # can start with the current users filter queryset
            # AuthorFormSet(queryset=Author.objects.filter(name__startswith='O'))
            event = Event.objects.get(event_name=request.GET.get('event'))
            formset = prefill_form(request)

            args = {'formset': formset, 'event': event, 'errors': errors}
            return render(request, 'events/event_register.html', args)

    else:

        event = Event.objects.get(event_name=request.GET.get('event'))
        codes = dict(Codes.objects.values_list('discount_code', 'discount_amount'))
        print(codes)
        codes = json.dumps(codes)
        print(codes)


        formset = prefill_form(request)

        args = {'formset': formset, 'event': event, 'codes': codes}
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
