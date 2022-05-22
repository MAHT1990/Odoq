from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display=["code", "season", "img", "aswr", "upload_date"]
    list_display_links=["code", "season", "img", "upload_date"]

    class Meta:
        ordering = ["-upload_date"]
    