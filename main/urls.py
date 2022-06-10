from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('answer_post/', views.answer_post, name='answer_post'),
    path('comment/new/', views.comment_new, name='comment_new')
    ]
