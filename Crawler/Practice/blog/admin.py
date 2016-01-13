from django.contrib import admin
from blog.models import UserInfo, AudioInfo

class UserInfo_admin(admin.ModelAdmin):
    list_display = ('id', 'name', 'psw', 'e_mail')
admin.site.register(UserInfo, UserInfo_admin)


class AudioInfo_admin(admin.ModelAdmin):
    list_display = ('title', 'date', 'mp3_time', 'mp3_path', 'pic_path', 'content_zg', 'content_en')
admin.site.register(AudioInfo, AudioInfo_admin)