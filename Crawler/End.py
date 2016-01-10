__author__ = 'carrie'
#coding=utf-8

from Start import GetUrlMethod, PatStoryMethod
import re
from urllib import urlopen

class PatStory():

    #获取每部影片首链接
    def getAllUrl(self):
        text = urlopen('http://www.kekenet.com/video/movie/').read()
        text = str(text).replace('\r\n','')
        video_list = []
        menu_list = []
        mlist = re.findall(r'<li><a href="/menu/.*?</li>',text)
        vlist = re.findall(r'<li><a href="/video/.*?</li>',text)
        dict = {'1': vlist, '2': mlist}
        for key in dict:
            for i in dict[key]:
                content = i.replace('<.*?>','')
                content = 'http://www.kekenet.com' + content
                if key == '1':
                    video_list.append(content)
                else:
                    menu_list.append(content)
        url_dict = {"video": video_list, "menu": menu_list}
        return url_dict

    #获取每部影片链接的页数
    def totalNum(self):
        url_dict = self.getAllUrl()
        video_list = url_dict['video']
        menu_list = url_dict['menu']
        video_num = []
        menu_num = []
        for key in url_dict:
            for url in url_dict[key]:
                text = urlopen(url).read()
                text = str(text).replace('\r\n', '')
                num = re.findall(r'<span id="total">.*?</span>',text)
                num = re.sub(r'<.*?>', '', num[0])
                if key == 'video':
                    video_num.append(num)
                else:
                    menu_list.append(num)
        num_dict = {'video': video_num, 'menu': menu_num}
        return num_dict

    #获取网页全部链接
    def getPageUrl(self):
        url_dict = self.getAllUrl()
        num_dict = self.totalNum()
