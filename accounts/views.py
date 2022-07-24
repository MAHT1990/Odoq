from django.shortcuts import render
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

# Create your views here.

def get_login_form():
    content = {
        'login_form' : AuthenticationForm()
    }

    return content

login = LoginView.as_view(
        template_name='main/index.html'
        )

logout = login_required(LogoutView.as_view())