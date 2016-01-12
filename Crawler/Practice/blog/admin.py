from django.contrib import admin
from blog.models import UserInfo

class UserInfo_admin(admin.ModelAdmin):
    list_display = ('id','name','psw','e_mail')
admin.site.register(UserInfo, UserInfo_admin)
