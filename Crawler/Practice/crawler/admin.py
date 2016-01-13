#coding=utf-8
from django.contrib import admin
from crawler.models import Audio


class Audio_admin(admin.ModelAdmin):
    list_display = ('title', 'date', 'mp3_time', 'mp3_path', 'pic_path', 'content')
admin.site.register(Audio, Audio_admin)