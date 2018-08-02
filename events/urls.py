from django.urls import path

from . import views

from django.contrib.auth.models import User

from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views


# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Authentication

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='events/login.html')),
]
