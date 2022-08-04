from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.forms import UsernameField

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext, gettext_lazy as _

from .models import UserProfile

User = get_user_model()

class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "ID와 비밀번호를 확인해주십시오."
        ),
        'inactive': _("This account is inactive."),
    }

class OdoqCreationForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].label = "ID"
            self.fields[self._meta.model.USERNAME_FIELD].error_messages = {
                'unique': _("같은 아이디가 이미 존재합니다."),
            }
            self.fields[self._meta.model.USERNAME_FIELD].help_text = "문자 / 숫자 / @ / . / + / - / _ 만 사용가능합니다."
    
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
    )

    nickname = forms.CharField(label='닉네임', min_length=2, max_length=10)

## Profile Form
class UserProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nickname'].label = "닉네임"
        
    class Meta:
        model = UserProfile
        fields = [
            'nickname'
        ]