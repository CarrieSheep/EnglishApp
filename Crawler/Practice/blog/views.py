from django.shortcuts import render
#coding=utf-8
from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponse

#创建表单,类UserForm的父类是forms模块里的Form对象
class UserForm(forms.Form):
    name = forms.CharField(max_length=50)
    psw = forms.IntegerField(max_value= 100)


def register(req):
    if req.method == 'POST':    #判定数据提交的方法
        user = UserForm(req.POST)   #表单对象的绑定
        if user.is_valid :  #验证提交的数据是否有效
            # print user.cleaned_data     #将数据放在user对象的cleaned_data的字典里
            return HttpResponse('OK')
    else:
        user = UserForm()
    return render_to_response('register.html', {'user':user})


