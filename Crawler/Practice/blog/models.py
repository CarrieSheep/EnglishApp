from django.db import models
#coding=utf-8


class UserInfo(models.Model):
    name = models.CharField(max_length=50)
    psw = models.IntegerField()
    e_mail = models.EmailField()

    def __unicode__(self):
        return self.name


class AudioInfo(models.Model):
    #音频标题
    title = models.CharField(max_length=100)
    #音频上传日期
    date = models.DateTimeField()
    #音频时长
    mp3_time = models.CharField(max_length=30)
    #音频存储路径
    mp3_path = models.FileField()
    #音频图片存储路径
    pic_path = models.ImageField()
    #音频中文字幕
    content_zg = models.TextField()
    #音频英文字幕
    content_en = models.TextField()

    def __unicode__(self):
        return self.title