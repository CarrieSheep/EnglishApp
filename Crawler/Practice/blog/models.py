from django.db import models
#coding=utf-8


class UserInfo(models.Model):
    name = models.CharField(max_length=50)
    psw = models.IntegerField()
    e_mail = models.EmailField()

    def __unicode__(self):
        return self.name


class Title(models.Model):
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title