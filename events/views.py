from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def home(request):
    name = "Name Here"
    numbers = {1, 2, 3, 4, 5}
    context = {'name': name, 'numbers': numbers}

    return render(request, 'events/home.html', context)


def login(request):
    return render(request, 'events/login.html')

