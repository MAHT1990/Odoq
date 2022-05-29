from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display=["code", "season", "img", "aswr", "upload_datetime"]
    list_display_links=["code", "season", "img", "upload_datetime"]

    class Meta:
        ordering = ["-upload_datetime"]


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ["season", "img"]
    list_display_links=["season", "img"]

    class Meta:
        ordering = ["season"]
