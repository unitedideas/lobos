from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from events.forms import MyAuthenticationForm


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='events/login.html', authentication_form =MyAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='events/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('merchandise/', views.merchandise, name='merchandise'),
    path('merchCheckout/', views.merchCheckout, name='merchCheckout'),
    path('registration_check/', views.registration_check, name='registration_check'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='events/reset_password.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='events/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='events/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='events/password_reset_complete.html'), name='password_reset_complete'),
    path('profile/password/', auth_views.PasswordChangeView.as_view(template_name='events/password_change.html'), name='password_change'),
    path('event-confirmation/', views.event_confirmation, name='event_confirmation'),
    path('event-registration/', views.event_register, name='event_register'),
    path('event-registration/<event>', views.event_register, name='event_register'),
    path('event_formset', views.event_formset, name='event_formset'),
    path('error_checking', views.error_checking, name='error_checking'),
    path('profile/password/done', auth_views.PasswordChangeDoneView.as_view(template_name='events/password_change_done.html'), name='password_change_done'),
    path('adminemail/', views.adminemail, name='adminemail'),
]