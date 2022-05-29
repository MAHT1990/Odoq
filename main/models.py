from enum import auto
from django.db import models

# Create your models here.

class Question(models.Model):
    code = models.CharField(max_length=255)
    season = models.IntegerField()
    img = models.ImageField()
    aswr = models.CharField(max_length=255)
    upload_datetime = models.DateTimeField(null=True) #업로드 예정일시
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now = True, null=True)
    
    def __str__(self):
        return self.code

class Notice(models.Model):
    season = models.IntegerField()
    img = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)