from django.db import models

from django.contrib.auth import get_user_model

from main.models import Comment, Cocomment

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(null=False, max_length=20)

    like_comments = models.ManyToManyField(Comment, blank=True, related_name='like_users', default=None)
    like_cocomments = models.ManyToManyField(Cocomment, blank=True, related_name='like_users', default=None)