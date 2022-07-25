from django.shortcuts import render

from django.conf import settings

from django.views.generic.edit import CreateView

from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)

from .forms import LoginForm, CreationForm

from main.views import get_content

User = get_user_model()

# Create your views here.


## LoginView Customizing
class OdoqLoginView(LoginView):

    """ 
    form_invalid가 main.views의 get_content를 import해서
    main 페이지 load시의 <Dictionary : content>를 받을 수 있도록.
    """ 
    def get(self, request, *args, **kwargs):

        main_views = __import__('main.views', fromlist=[''])
        #DEBUG
        debug_title = 'accounts.views.OdoqLoginView.get'
        len_debug_title = len(debug_title)
        print('=' * len_debug_title,'\n',debug_title,'\n','=' * len_debug_title)

        print(super())
        print(type(self.get_context_data()))
        print(type(main_views.get_content))
        print(main_views.get_content())
        print(self.get_context_data())
        return self.render_to_response(self.get_context_data())

    def form_invalid(self, form):

        #DEBUG
        #Debug Log
        debug_title = 'accounts.views.OdoqLoginView.form_invalid'
        len_debug_title = len(debug_title)
        print('=' * len_debug_title,'\n',debug_title,'\n','=' * len_debug_title)
        print(type(self.get_context_data(form=form)))
        print(self.get_context_data(form=form))

        #TODO 왜 get_content 호출이 불가능한가.
        #main APP <Class : indexView > 만들어서 다시.

        return self.render_to_response(self.get_context_data(form=form))

login = OdoqLoginView.as_view(
        template_name='main/index.html'
        )

## LogoutView
logout = login_required(LogoutView.as_view())



## CreateView
signup = CreateView.as_view(
    model = User,
    form_class = CreationForm,
    success_url = settings.LOGIN_URL,
)
