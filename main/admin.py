from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe


@admin.register(OnOff)
class OnOffAdmin(admin.ModelAdmin):
    list_display = ["title", "on_off", "off_img_tag"]
    list_editable = ["on_off"]

    def off_img_tag(self, o):
        if o.off_img:
            return mark_safe(f'<a href="{o.off_img.url}" target="_blank" rel="noopener noreferrer"><img src="{o.off_img.url}" style="width:200px"/></a>')

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ["season", "img_tag", "created_at", "updated_at"]
    list_display_links=["season", "img_tag"]

    def img_tag(self, notice):
        if notice.img:
            return mark_safe(f'<a href="{notice.img.url}" target="_blank" rel="noopener noreferrer"><img src="{notice.img.url}" style="width:200px"/></a>')

    class Meta:
        ordering = ["created_at"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display=["code", "season", "img", "img_tag", "aswr", "upload_datetime"]
    list_display_links=["code", "season", "upload_datetime"]
    list_editable = ["img"]

    def img_tag(self, question):
        if question.img:
            return mark_safe(f'<a href="{question.img.url}" target="_blank" rel="noopener noreferrer"><img src="{question.img.url}" style="width:200px"/></a>')
    class Meta:
        ordering = ["-upload_datetime"]



@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ["phone_number"]