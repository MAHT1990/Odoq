from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.forms import UsernameField

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.utils.translation import gettext, gettext_lazy as _

User = get_user_model()

class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "ID와 비밀번호를 확인해주십시오."
        ),
        'inactive': _("This account is inactive."),
    }

class CreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _('두 비밀번호가 일치하지않습니다.'),
    }

    password1 = forms.CharField(
        label=_("비밀번호"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("비밀번호 확인"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}

    nickname = forms.CharField(label='닉네임', min_length=2, max_length=10)