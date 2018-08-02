from django.urls import path
from . import views
from django.contrib.auth import views as auth_views, logout

# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Authentication

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='events/login.html'), name='login'),
    path('logout/', auth_views.LoginView.as_view(template_name='events/logout.html'), name='logout'),
    path('register/', views.register, name='register'),

]
