__author__ = 'carrie'
#coding=utf-8
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Practice.settings')
import django
django.setup()

from Start import GetUrlMethod, PatStoryMethod
from blog.models import AudioInfo

class PatMaritimePianist():

     #爬取网页链接
    def getPageUrl(self):
        startUrl = 'http://www.kekenet.com/video/movie/piano/'
        method = GetUrlMethod()
        page_list = method.getPageUrl(0, startUrl)
        # print 1, page_list
        return page_list

    def getStoryAndMp3UrlAndTitle(self):
        page_list = self.getPageUrl()
        method = GetUrlMethod()
        dict = method.getStoryAndMP3UrlAndTitle(page_list, 'video')
        story_list = dict['story']
        mp3_list = dict['mp3']
        # print 3, len(story_list), story_list
        # print 3, len(mp3_list), mp3_list
        return dict

    def getArticle(self):
        dict = self.getStoryAndMp3UrlAndTitle()
        story_list = dict['story']
        mp3_list = dict['mp3']
        title_list = dict['title']
        for index in range(0, len(story_list)):
            url = story_list[index]
            patstory = PatStoryMethod()
            sc = patstory.getStorySC(url)
            content_dict = patstory.getContent(sc)
            if content_dict != {}:
                title = title_list[index]
                print 1, title
                date = patstory.getDate(sc)
                print 2, date
                mp3_dict = patstory.getMP3AndTime(mp3_list[index], index, 'MaritimePianist')
                print 3, mp3_dict['mp3_time']
                print 4, mp3_dict['mp3_path']
                pic = "http://pic.kekenet.com/2012/0223/20120223034042496.jpg"
                pic_path = patstory.getPicture(sc, index, 'MaritimePianist', pic)
                print 5, pic_path
                content_zg = content_dict['en']
                content_en = content_dict['zg']
                print 6, content_en
                print 7, content_zg
                print '\n'
                AudioInfo.objects.create(title=title, date=date, mp3_time=mp3_dict['mp3_time'],
                                         mp3_path=mp3_dict['mp3_path'], pic_path=pic_path,
                                         content_zg=content_dict['zg'], content_en=content_dict['en'])




if __name__ == '__main__':
    a = PatMaritimePianist()
    a.getArticle()
