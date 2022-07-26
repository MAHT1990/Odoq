from django.urls import path, include

from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='main:index',)),
    path('login/',views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signin/', views.signin, name='signin'),
    ]