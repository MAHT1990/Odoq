from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)

from .forms import (
    LoginForm, OdoqCreationForm, UserProfileForm
)
from .models import UserProfile

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

        # debug_title = 'accounts.views.OdoqLoginView.get'
        # len_debug_title = len(debug_title)
        # print('=' * len_debug_title,'\n',debug_title,'\n','=' * len_debug_title)

        #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG 


        return self.render_to_response(context)

    def form_invalid(self, form):

        index = IndexView(get_login_form_bool = False)

        context = self.get_context_data()
        context.update(index.get_content())


        #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG
        
        # debug_title = 'accounts.views.OdoqLoginView.form_invalid'
        # len_debug_title = len(debug_title)
        # print('=' * len_debug_title,'\n',debug_title,'\n','=' * len_debug_title)

        #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG #DEBUG


        return self.render_to_response(context)

login = OdoqLoginView.as_view(
        form_class = LoginForm,
        template_name='main/index.html',
        )


## LogoutView
logout = login_required(LogoutView.as_view())



## CreateView

class OdoqCreateView(CreateView):
    def form_valid(self, form):
        self.object = form.save() # user_instance 생성

        nickname = form.cleaned_data['nickname'] 
        UserProfile.objects.create(user=self.object, nickname = nickname)

        return HttpResponseRedirect(self.get_success_url())
        

signin = OdoqCreateView.as_view(
    model = User,
    form_class = OdoqCreationForm,
    template_name = 'accounts/user_creation_form.html',
    success_url = settings.LOGIN_REDIRECT_URL,
)

## Profile View

@login_required
def userprofile(request):
    try:
        userprofile = request.user.userprofile
    except UserProfile.DoesNotExist:
        userprofile = None

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            userprofile = form.save(commit = False)
            userprofile.user = request.user
            username = request.POST['username']
            password = request.POST['password']
            if authenticate(request=request, username = username, password = password) == userprofile.user:
                userprofile.save()
                return redirect('main:index')
            else:
                form = UserProfileForm(instance = userprofile)
                return render(request, 'accounts/user_profile_form.html', {
                    'form':form,
                    'error_message':'비밀번호가 일치하지 않습니다.'
                })
        else:
            return render(request, 'accounts/user_profile_form.html', {
                    'form':form,
                })          

    else:
        form = UserProfileForm(instance = userprofile)
        return render(request, 'accounts/user_profile_form.html', {
            'form':form,
        })
