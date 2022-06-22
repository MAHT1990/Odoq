from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(OnOff)
class OnOffAdmin(admin.ModelAdmin):
    list_display = ["title", "on_off"]
    list_editable = ["on_off"]

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ["season", "img", "created_at", "updated_at"]
    list_display_links=["season", "img"]

    class Meta:
        ordering = ["created_at"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display=["code", "season", "img", "aswr", "upload_datetime"]
    list_display_links=["code", "season", "img", "upload_datetime"]

    class Meta:
        ordering = ["-upload_datetime"]



@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ["phone_number"]