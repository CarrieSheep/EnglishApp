from django.db import models
#coding=utf-8

class Audio(models.Model):
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
    #音频中英字幕
    content = models.TextField()


    def __unicode__(self):
        return self.title