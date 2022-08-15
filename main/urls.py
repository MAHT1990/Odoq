from django.urls import path, include
from . import views
from . import views_proto

urlpatterns = [
    path('',views.index, name='index'),
    path('answer_post/', views.answer_post, name='answer_post'),
    path('sms_new/', views.sms_new, name='sms_new'),
    path('sms_delete/', views.sms_delete, name='sms_delete'),
    path('comment/new/', views.comment_new, name = 'comment_new'),
    path('comment/edit/', views.comment_edit, name = 'comment_edit'),
    path('comment/delete/', views.comment_delete, name = 'comment_delete'),
    path('comment/like/<int:comment_id>/<int:zero_xor_one>/', views.like, name = 'comment_like'),
    path('comment/<str:queryset_filter>/<str:queryset_order>/', views.index, name='filtering_and_ordering'),
    path('cocomment/new/', views.cocomment_new, name = 'cocomment_new'),
    path('cocomment/delete/', views.cocomment_delete, name = 'cocomment_delete'),
    path('cocomment/edit/', views.cocomment_edit, name = 'cocomment_edit'),
    path('cocomment/like/<int:cocomment_id>/<int:zero_xor_one>/', views.like, name = 'cocomment_like'),
    ] + [
        path('proto/comments/', views_proto.all_comments, name = 'all_comments'),
    ]
