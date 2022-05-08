from django.db import models

# Create your models here.

class Question(models.Model):
    season = models.IntegerField()
    code = models.CharField(max_length=255)
    img = models.ImageField()
    aswr = models.CharField(max_length=255)
    
    def __str__(self):
        return self.code