from enum import auto
from django.db import models
from django.core.validators import MinLengthValidator

from django.contrib.auth import get_user_model

User = get_user_model()

class OnOff(models.Model):
    title = models.CharField(max_length=255)
    on_off = models.BooleanField()
    off_img = models.ImageField(upload_to='season_off_img', blank=True)


class Notice(models.Model):
    season = models.CharField(max_length=255)
    img = models.ImageField(null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.text
    
    class Meta:
        ordering = ["-created_at"]


class Question(models.Model):
    code = models.CharField(max_length=255)
    season = models.CharField(max_length=255)
    img = models.ImageField()
    aswr = models.CharField(max_length=255)
    upload_datetime = models.DateTimeField(null=True) #업로드 예정일시
    
    answer_count = models.PositiveIntegerField(default=0) # 답안 제출수 
    solve_count = models.PositiveIntegerField(default=0) # 정답 수

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now = True, null=True)
    
    def __str__(self):
        return self.code


class Comment(models.Model):
    # Question과 Comment는 1 : n 의 관계이다.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    like_count = models.PositiveIntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['-created_at']

class PhoneNumber(models.Model):
    phone_number = models.CharField(max_length=13)

class Cocomment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.TextField()
    like_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

