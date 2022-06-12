from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('answer_post/', views.answer_post, name='answer_post'),
    path('sms_new/', views.sms_new, name='sms_new'),
    path('sms_delete/', views.sms_delete, name='sms_delete'),
    ]
