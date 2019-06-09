from .models import RiderProfile, Profile, Codes, Merchandise, MerchandiseOrder, ClubEvent
import json
from django.core.serializers.json import DjangoJSONEncoder
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
    MerchandiseOrderForm,
    RegistrationCheck,
    LobosRace
)
from django.db.models import F
from django.forms.utils import ErrorDict, ErrorList
from django.template import loader
from django.template import Context
from anymail.message import attach_inline_image_file
from django.template.loader import render_to_string
import random
import string
import json
from datetime import datetime as ddt
import datetime as dt


def clubeventsCheckout(request):
    return render(request, 'events/clubeventsCheckout.html')


def change_names_to_lower():
    all_names = RiderProfile.objects.all()
    for name in all_names:
        name.first_name = name.first_name.lower()
        name.last_name = name.last_name.lower()
        try:
            name.email = name.email.lower()
            name.email2 = name.email2.lower()
        except:
            print('no email')

        try:
            name.confirmation_number = name.confirmation_number.upper()
        except:
            print('no email')

        name.save()


@staff_member_required
def clubevents(request):
    if request.POST:
        form = LobosRace(request.POST)
        if form.is_valid():
            data = {
                'name': form.cleaned_data['name'],
                'event': 'Devils Head',
            }
            f = form.save()
            return render(request, 'events/clubeventsCheckout.html', {'data': data})
        else:
            errors = form.errors
            return render(request, 'events/clubevents.html', {'form': form, 'errors': errors})
    else:
        form = LobosRace()
        signed_up = len(ClubEvent.objects.all())
        return render(request, 'events/clubevents.html', {'form': form, 'signed_up': signed_up})


def registration_check(request):
    if request.POST:
        form = RegistrationCheck(request.POST)

        if form.is_valid():
            f = form.cleaned_data
            confirmation_number = f['confirmationNumber'].upper()
            first_name = f['first_name'].lower()
            last_name = f['last_name'].lower()

            if confirmation_number == '' and first_name == '' and last_name == '':
                form = RegistrationCheck()

                args = {
                    'result': False,
                    'name': first_name + " " + last_name,
                    'event': 'Please provide first and last name or a confirmation number'
                }
                return render(request, 'events/registration_check.html', {"args": args, 'form': form})

            if confirmation_number:
                try:
                    event_id = RiderProfile.objects.filter(
                        confirmation_number=confirmation_number).values_list('event_id', flat=True)

                    confirmation_names = RiderProfile.objects.filter(
                        confirmation_number=confirmation_number).values_list('first_name', 'last_name')

                    if event_id is not None:
                        confirmation_names = list(confirmation_names)
                        first_and_last_names = list((' '.join(name) for name in confirmation_names))
                        event_name = Event.objects.filter(id=event_id[0]).values_list('event_name', flat=True)
                        event_date = Event.objects.filter(id=event_id[0]).values_list('event_date', flat=True)
                        event_data = event_name[0] + ' scheduled for ' + event_date[0].strftime('%m/%d/%Y')
                        args = {
                            'result': True,
                            'name': first_and_last_names,
                            'event': event_data
                        }

                        return render(request, 'events/registration_check.html', {"args": args, 'form': form})
                except:
                    args = {
                        'result': False,
                        'name': ' ',
                        'event': 'That confirmation number was not found.'
                    }

                    return render(request, 'events/registration_check.html', {"args": args, 'form': form})

            elif first_name != '' and last_name != '':
                event_id = RiderProfile.objects.filter(first_name=first_name).filter(
                    last_name=last_name).values_list(
                    'event', flat=True).last()
                if event_id is not None:
                    first_and_last_names = [first_name + " " + last_name]
                    event_name = Event.objects.filter(id=event_id).values_list('event_name', flat=True)
                    event_date = Event.objects.filter(id=event_id).values_list('event_date', flat=True)
                    event_data = event_name[0] + ' scheduled for ' + event_date[0].strftime('%m/%d/%Y')

                    args = {
                        'result': True,
                        'name': first_and_last_names,
                        'event': event_data
                    }
                    return render(request, 'events/registration_check.html', {"args": args, 'form': form})

                else:
                    args = {
                        'result': True,
                        'name': first_name + ' ' + last_name,
                        'event': 'was not found.'
                    }

                    return render(request, 'events/registration_check.html', {"args": args, 'form': form})
            else:
                form = RegistrationCheck()

                args = {
                    'result': False,
                    'name': first_name + " " + last_name,
                    'event': 'was not found.'
                }
                return render(request, 'events/registration_check.html', {"args": args, 'form': form})

        else:
            errors = {
                'errors': form.errors
            }
            return render(request, 'events/registration_check.html', {'form': form, 'errors': errors})

    else:
        form = RegistrationCheck()
        return render(request, 'events/registration_check.html', {'form': form})


def merchCheckout(request):
    return render(request, 'events/merchCheckout.html')


def merchandise(request):
    merchValues = Merchandise.objects.filter(available_on_merch_page=True).values()
    count = 1
    merch = {}
    for dict in merchValues:
        itemInfo = {}
        sizeQty = {}
        itemName = "item_" + str(count)
        for attr, value in dict.items():
            if 'quantity_available' in attr:
                sizeQty[attr] = value
            else:
                itemInfo[attr] = value
        count += 1
        merch[itemName] = [itemInfo, sizeQty]

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = MerchandiseOrderForm(request.POST)

        if form.is_valid():
            postData = request.POST.dict()
            # save the data to the database
            # try:
            itemsOrderedDict = json.loads(postData['items_ordered'])
            item_ordered = itemsOrderedDict['transactions'][0]['item_list']['items']
            all_items = ''
            paypal_order_id = itemsOrderedDict['transactions'][0]['related_resources'][0]['sale']['id']

            if MerchandiseOrder.objects.filter(paypal_order_id=paypal_order_id).exists():
                args = {
                    "thing_key": paypal_order_id,
                }
                return render(request, 'events/merchCheckout.html', {"args": args})
            else:
                MerchandiseOrder.objects.create(
                    first_name=postData['first_name'],
                    last_name=postData['last_name'],
                    address=postData['address'],
                    city=postData['city'],
                    state=postData['state'],
                    zip_code=postData['zip_code'],
                    email=postData['email'],
                    date_ordered=itemsOrderedDict['create_time'],
                    paypal_order_id=paypal_order_id,
                    items_ordered=all_items)

                for item in item_ordered:
                    for key in item:
                        if key == 'name':
                            all_items += 'Item: ' + str(item[key]) + ' - '
                        if key == 'quantity':
                            quantity = item[key]
                            all_items += 'Quantity: ' + str(quantity) + '\n'
                        if key == 'sku':
                            quantity = item['quantity']
                            split_sku = item[key].split(' ')
                            pk = split_sku[0]
                            product = Merchandise.objects.get(pk=pk)
                            current_quantity = getattr(product, split_sku[1])
                            setattr(product, split_sku[1], current_quantity - quantity)
                            product.save()

                args = {
                    "thing_key": paypal_order_id,
                }
                return render(request, 'events/merchCheckout.html', {"args": args})

        else:
            args = {
                "merch": merch,
            }
            json_args = json.dumps(args)

            return render(request, "events/merchandise.html", {"args": args, "json_args": json_args, "form": form})

    else:
        form = MerchandiseOrderForm()
        args = {
            "merch": merch,
        }
        json_args = json.dumps(args)

        return render(request, "events/merchandise.html", {"args": args, "json_args": json_args, "form": form})


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
    events = Event.objects.all().order_by('-event_date')[0:2]
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
    promotion = []

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
        promotion.append(event.promotion)

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
                         promotion,  # 14
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
            username = first_name.lower() + last_name.lower() + \
                       email.lower().replace(" ", "")
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
            args = {
                'form': form, 'errors': 'A user with that username already exists. Please choose a different one.'}
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

            text_content = 'Hi ' + first_name.title() + \
                           '\nYou recently requested to reset your password at LobosEvents.com. \n' \
                           'Your username, in case you\'ve forgotten: ' + username

            html_content = 'Hi ' + first_name.title() + \
                           '\nYou recently requested to reset your password at LobosEvents.com. \n' \
                           'Your username, in case you\'ve forgotten: ' + username

            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return redirect('/profile/')
        else:
            # changed this from formset.errors to form.errors
            # errors = {'errors': formset.errors}
            errors = {'errors': form.errors}
            return redirect('change_password', errors)
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'events/password_change.html', args)


def error_checking(request):
    under_16 = 0
    escorts_signed_up = 0
    over_16 = False
    forms = json.load(request)  # The form as html string
    event_date = forms["event_date"].replace(",", "")
    event_date = ddt.strptime(event_date, '%B %d %Y')
    event_date = ddt.date(event_date)
    form_count = 0
    formset = RiderProfileFormSet(forms)

    if formset.is_valid():
        # calc age
        for form in formset:
            form_count += 1
            y = 0
            m = 0
            d = 0
            age_error = False
            email1 = form.cleaned_data['email']
            email2 = form.cleaned_data['email2']
            birth_date = form.cleaned_data['birth_date']
            rider_class = form.cleaned_data['rider_class']

            gender = form.cleaned_data['gender']
            y = event_date.year - birth_date.year
            m = event_date.month - birth_date.month
            d = event_date.day - birth_date.day

            #  under 16 rider classes

            class_list_under_16 = ["Expert under 16 AA", "Expert under 16 Open Expert", "Expert under 16 250 EX",
                                   "Amateur under 16 Open Amateur", "Amateur under 16 250 AM",
                                   "Amateur under 16 Sportsman", "Amateur under 16 Beginner", "Amateur under 16 Women",
                                   "Amateur under 16 Jr."]
            class_list_under_30 = ["Expert under 16 AA", "Expert under 16 Open Expert", "Expert under 16 250 EX",
                                   "Amateur under 16 Open Amateur", "Amateur under 16 250 AM",
                                   "Amateur under 16 Sportsman", "Amateur under 16 Beginner", "Amateur under 16 Women",
                                   "Amateur under 16 Jr.",
                                   "Expert 16 and over 30 EX", "Expert 16 and over 40 EX-EX",
                                   "Amateur 16 and over 30 AM", "Amateur 16 and over 40 EX-AM",
                                   "Amateur 16 and over 40 AM", "Amateur 16 and over 50 AM",
                                   "Amateur 16 and over 50 EX", "60 Class",
                                   "70 Class"]
            class_list_under_40 = ["Expert under 16 AA", "Expert under 16 Open Expert", "Expert under 16 250 EX",
                                   "Amateur under 16 Open Amateur", "Amateur under 16 250 AM",
                                   "Amateur under 16 Sportsman", "Amateur under 16 Beginner", "Amateur under 16 Women",
                                   "Amateur under 16 Jr.", "Expert 16 and over 40 EX-EX",
                                   "Amateur 16 and over 40 EX-AM", "Amateur 16 and over 40 AM",
                                   "Amateur 16 and over 50 AM", "Amateur 16 and over 50 EX", "60 Class",
                                   "70 Class"]
            class_list_under_50 = ["Expert under 16 AA", "Expert under 16 Open Expert", "Expert under 16 250 EX",
                                   "Amateur under 16 Open Amateur", "Amateur under 16 250 AM",
                                   "Amateur under 16 Sportsman", "Amateur under 16 Beginner", "Amateur under 16 Women",
                                   "Amateur under 16 Jr.", "Amateur 16 and over 50 AM", "Amateur 16 and over 50 EX",
                                   "60 Class",
                                   "70 Class"]
            class_list_under_60 = ["Expert under 16 AA", "Expert under 16 Open Expert", "Expert under 16 250 EX",
                                   "Amateur under 16 Open Amateur", "Amateur under 16 250 AM",
                                   "Amateur under 16 Sportsman", "Amateur under 16 Beginner", "Amateur under 16 Women",
                                   "Amateur under 16 Jr.", "60 Class", "70 Class"]
            class_list_under_70 = ["Expert under 16 AA", "Expert under 16 Open Expert", "Expert under 16 250 EX",
                                   "Amateur under 16 Open Amateur", "Amateur under 16 250 AM",
                                   "Amateur under 16 Sportsman", "Amateur under 16 Beginner", "Amateur under 16 Women",
                                   "Amateur under 16 Jr.", "70 Class"]

            rider_class_check = False
            age_set = [30, 40, 50, 60, 70]
            content = {}
            if email1 != email2:
                content['email_not_the_same'] = True
                content["email_not_the_same_form"] = form_count

            if y > 150:
                content['birthdate_wrong'] = True
                content["birthdate_form"] = form_count
                # return JsonResponse(content)

            if (y < 16) or (y == 16 and m < 0) or (y == 16 and m == 0 and d < 0):
                under_16 += 1
                if rider_class not in class_list_under_16:
                    content['under_class_age'] = {
                        "rider_class": rider_class, 'form': form_count}
                    content["age_error"] = True
                else:
                    pass
            else:
                over_16 = True

            if rider_class == "Escort Rider" and over_16 == True:
                escorts_signed_up += 1

        if (under_16 - escorts_signed_up > 0):
            error = 'escorts' if (
                    under_16 - escorts_signed_up > 1) else 'escort'
            content['escorts_signed_up'] = escorts_signed_up
            content['under_16'] = under_16
            # return JsonResponse(content)

        # age vs rider_class check
        # if ((y < 16) or (y == 16 and m < 0) or (y == age and m == 0 and d < 0)) and ( rider_class not in class_list_under_16):
        #     print('RIDER CLASS NOT GOOD... less than age ' + str(age) + " rider in " + rider_class)
        #     content['under_class_age'] = {"age": age, "rider_class": rider_class, 'form': form_count}
        #     content["age_error"] = True

        for age in age_set:
            if (y < age and y >= 16) or (y == age and m < 0) or (y == age and m == 0 and d < 0):
                if (age == 30 and rider_class in class_list_under_30) or \
                        (age == 40 and rider_class in class_list_under_40) or \
                        (age == 50 and rider_class in class_list_under_50) or \
                        (age == 60 and rider_class in class_list_under_60) or \
                        (age == 70 and rider_class in class_list_under_70):
                    content['under_class_age'] = {
                        "age": age, "rider_class": rider_class, 'form': form_count}
                    content["age_error"] = True
                    # return JsonResponse(content)

        if gender == 'Male' and (rider_class == 'Amateur under 16 Women' or rider_class == "Amateur 16 and over Women"):
            content['gender_class'] = True
            content['gender_form'] = form_count
            # return JsonResponse(content)
        if content != {}:
            return JsonResponse(content)

        else:
            content = {'success': True}
            return JsonResponse(content)

    else:
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
            postData = request.POST.dict()
            itemsOrderedDict = json.loads(postData['form-0-items_ordered'])
            confirmation_number = itemsOrderedDict['transactions'][0]['related_resources'][0]['sale']['id']
            confirmation_number = confirmation_number.upper()

            if RiderProfile.objects.filter(confirmation_number=confirmation_number).exists():
                args = {
                    "confirmation_number": confirmation_number,
                }
                return render(request, 'events/event_resubmited.html', {"args": args})

            count = 0
            confirm = {}
            for form in formset:
                # print(form.items_ordered)
                count += 1
                created_username = form.first_name + form.last_name + form.email
                created_username = created_username.replace(" ", "").lower()
                form.confirmation_number = confirmation_number
                form.event = Event.objects.get(
                    event_name=request.GET.get('event'))
                event = str(form.event)

                if form.discount_code != None:
                    usedCode = form.discount_code
                    Codes.objects.filter(discount_code=usedCode).delete()

                if User.objects.filter(username=created_username).exists():
                    user_id = User.objects.get(username=created_username).id

                if not User.objects.filter(username=created_username).exists():
                    user = User.objects.create(username=created_username,
                                               email=form.email,
                                               first_name=form.first_name,
                                               last_name=form.last_name, )

                    user.first_name = form.first_name.lower()
                    user.last_name = form.last_name.lower()
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
                    user.update(
                        emergency_contact_name=form.emergency_contact_name)
                    user.update(
                        emergency_contact_phone=form.emergency_contact_phone)

                    message = ''
                    username = created_username
                    first_name = form.first_name.lower()
                    last_name = form.last_name.lower()
                    email = form.email.lower()
                    rider_class = form.rider_class

                    confirm[created_username] = {'message': message,
                                                 'username': username,
                                                 'first_name': first_name.title(),
                                                 'last_name': last_name.title(),
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
                    first_name = form.first_name.lower()
                    last_name = form.last_name.lower()
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
                                                 'first_name': first_name.title(),
                                                 'last_name': last_name.title(),
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
                    first_name = form.first_name.lower()
                    last_name = form.last_name.lower()
                    email = form.email.lower()
                    rider_class = form.rider_class

                    confirm[created_username] = {'username': username,
                                                 'first_name': first_name.title(),
                                                 'last_name': last_name.title(),
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
            event = Event.objects.get(event_name=request.GET.get('event'))
            formset = prefill_form(request)

            args = {'formset': formset, 'event': event, 'errors': errors}
            return render(request, 'events/event_register.html', args)

    else:
        # formset = prefill_form(request)
        event = Event.objects.get(event_name=request.GET.get('event'))
        rider_limit = event.rider_limit
        registered_riders = len(RiderProfile.objects.filter(event=event))

        if rider_limit - registered_riders <= 0:
            args = {'event': event}
            return render(request, 'events/sold_out.html', args)

        if not event.open_registration:
            args = {'event': event}
            return render(request, 'events/unavailable_event.html', args)

        codes = dict(Codes.objects.values_list(
            'discount_code', 'discount_amount'))
        codes = json.dumps(codes)

        args = {'event': event, 'codes': codes}
        # args = {'formset': formset, 'event': event, 'codes': codes}
        return render(request, 'events/event_register.html', args)


def event_confirmation(request):
    args = {'request': request, 'user': request.user}
    return render(request, 'events/event_confirmation.html', args)


def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def event_formset(request):
    formset = prefill_form(request)
    formset = str(formset)
    event = json.loads(request.body)['event']
    event_date = json.loads(request.body)['event'][-4:]
    escort_rider_cost = Event.objects.get(
        event_name=event, event_date__contains=event_date).escort_rider_cost
    reg_rider_cost = Event.objects.get(
        event_name=event, event_date__contains=event_date).pre_entry_cost
    # reg_rider_cost = Event.objects.get(event_name=request.GET.get('event')).pre_entry_cost
    formset_to_vue = {'reg_rider_cost': reg_rider_cost,
                      'escort_rider_cost': escort_rider_cost, 'formset': formset}
    return JsonResponse(formset_to_vue)


def prefill_form(request):
    # form_fill_dict = {}
    # profile_field_names = []
    # prof = request.user.profile

    # for field in Profile._meta.get_fields():
    #     if field.name is not 'id':
    #         profile_field_names.append(field.name)
    #         field = str(field.name)
    #         form_fill_dict[field] = getattr(prof, field)

    # user_field_names = ['first_name', 'last_name', 'email']
    # user_prof = request.user
    # for field in User._meta.get_fields():
    #     field = str(field.name)
    #     if field in user_field_names:
    #         form_fill_dict[field] = getattr(user_prof, field)
    # print(form_fill_dict)
    # print(RiderProfileFormSet(queryset=RiderProfile.objects.none()))
    # return RiderProfileFormSet(queryset=RiderProfile.objects.none(), initial=[form_fill_dict])
    return RiderProfileFormSet(queryset=RiderProfile.objects.none())
