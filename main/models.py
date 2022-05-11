from django.db import models

# Create your models here.

class Question(models.Model):
    code = models.CharField(max_length=255)
    season = models.IntegerField()
    img = models.ImageField()
    aswr = models.CharField(max_length=255)
    
    def __str__(self):
        return self.code