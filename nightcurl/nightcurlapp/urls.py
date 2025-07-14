from nightcurlapp.views import UserRegistrationView, LogoutView, UserLoginView,activate
from django.contrib import admin
from django.urls import path , include
from nightcurlapp import views
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .views import HomeView


app_name = 'nightcurlapp'

urlpatterns = [
    path(
        "login/", UserLoginView.as_view(),
        name="login"
    ),
    path(
        "logout/", LogoutView.as_view(),
        name="user_logout"
    ),
    path(
        "signup/", UserRegistrationView.as_view(),
        name="signup"
    ),
     path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='nightcurlapp/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='nightcurlapp/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='nightcurlapp/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='nightcurlapp/password_reset_complete.html'), name='password_reset_complete'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='nightcurlapp/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='nightcurlapp/password_change_done.html'), name='password_change_done'),
    ]