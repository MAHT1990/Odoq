from enum import auto
from django.db import models

class OnOff(models.Model):
    title = models.CharField(max_length=255)
    on_off = models.BooleanField()


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
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now = True, null=True)
    
    def __str__(self):
        return self.code


class Comment(models.Model):
    # Question과 Comment는 1 : n 의 관계이다.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

class PhoneNumber(models.Model):
    phone_number = models.CharField(max_length=13)