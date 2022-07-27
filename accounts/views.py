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

from main.views import IndexView


User = get_user_model()


## LoginView Customizing
class OdoqLoginView(LoginView):

    """ 
    /accounts/login 으로 get 으로 들어올 때,
    /accounts/login 으로 POST의 form이 invalid일때,

    form_invalid가 main.views의 get_content를 import해서
    main 페이지 load시의 <Dictionary : content>를 받을 수 있도록.
    """ 

    def get(self, request, *args, **kwargs):

        index = IndexView(get_login_form_bool = False)

        context = self.get_context_data()
        context.update(index.get_content())


        #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG 

        debug_title = 'accounts.views.OdoqLoginView.get'
        len_debug_title = len(debug_title)
        print('=' * len_debug_title,'\n',debug_title,'\n','=' * len_debug_title)

        #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG 


        return self.render_to_response(context)

    def form_invalid(self, form):

        index = IndexView(get_login_form_bool = False)

        context = self.get_context_data()
        context.update(index.get_content())


        #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG
        
        debug_title = 'accounts.views.OdoqLoginView.form_invalid'
        len_debug_title = len(debug_title)
        print('=' * len_debug_title,'\n',debug_title,'\n','=' * len_debug_title)

        #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG


        return self.render_to_response(context)

login = OdoqLoginView.as_view(
        form_class = LoginForm,
        template_name='main/index.html',
        )


## LogoutView
logout = login_required(LogoutView.as_view())



## CreateView
signin = CreateView.as_view(
    model = User,
    form_class = CreationForm,
    template_name = 'accounts/user_form.html',
    success_url = settings.LOGIN_URL,
)
