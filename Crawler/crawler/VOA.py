__author__ = 'carrie'
#coding=utf-8

from K_Method import GetUrlMethod, PatStoryMethod
import chardet
from urllib import urlopen
import re

class PatVoA():

    def getUrl(self):
        startUrl_list = ['http://www.kekenet.com/broadcast/Normal/Oct14/',
                         'http://www.kekenet.com/broadcast/Normal/Sep14/',
                         'http://www.kekenet.com/broadcast/Normal/Aug14/',
                         'http://www.kekenet.com/broadcast/Normal/Jul14/',
                         'http://www.kekenet.com/broadcast/Normal/Jun14/',
                         'http://www.kekenet.com/broadcast/Normal/May14/',
                         'http://www.kekenet.com/broadcast/Normal/Apr14']
        fnum_list = [1, 1, 1, 1, 1, 3, 2, ]
        lnum_list = [3, 4, 4, 5, 5, 4, 4, ]
        page_list = []
        method = GetUrlMethod()
        # 获取网页url
        for index in range(0, len(startUrl_list)):
            page_url = method.getPageUrl(fnum_list[index], lnum_list[index], startUrl_list[index])
            for url in page_url:
                page_list.append(url)
        #获取每篇新闻的url,MP3下载地址,标题
        dict = method.getStoryAndMP3UrlAndTitle(page_list, 'broadcast')
        return dict

    def getArticle(self, id):
        dict = self.getUrl()
        news_list = dict['story']
        mp3_list = dict['mp3']
        title_list = dict['title']
        print len(title_list)
        num = 0
        for index in range(0, len(news_list)):
            url = news_list[index]
            patstory = PatStoryMethod()
            sc = patstory.getStorySC(url)
            lrc = r'/home/carrie/downloads/kekenet-VOA/lrc/' + str(index) + r'.lrc'  # 需更改路径
            mp3 = r'/home/carrie/downloads/kekenet-VOA/mp3/' + str(index) + r'.mp3' # 需更改路径
            jpg_path = '/home/carrie/downloads/kekenet-VOA/picture/' +str(index) + '.jpg' # 需更改路径
            png_path = '/home/carrie/downloads/kekenet-VOA/picture/' + str(index) + '.png' # 需更改路径
            default_path = '/home/carrie/downloads/kekenet-VOA/picture/default.jpg'
            lrc_path = patstory.getLrc(mp3_list[index], lrc)
            if lrc_path != '':
                #判断文本是否有中文翻译,目的减少MP3下载
                text = urlopen(lrc_path).read()
                c = chardet.detect(text)
                code = c['encoding']
                text = str(text).decode(code, 'ignore').encode('utf-8').replace('\n', '')
                text = text.decode('utf-8')
                a = re.findall(u'[\u4e00-\u9fa5]', text)
                if len(a) >= 100:
                    mp3_dict = patstory.getMP3AndTime(mp3_list[index], mp3)
                    #判断音频长度是否短于5分钟
                    if mp3_dict['mp3_time'] <= 300:
                        total_time = mp3_dict['mp3_time'] * 1000
                        content_dict = patstory.getContent(lrc_path, total_time)
                        # 判断
                        if content_dict['content'] != '':
                            print 'id: ', id
                            type = 'news'
                            print 'type: ', type
                            title = patstory.getTitle(title_list[index])
                            print 'title: ', title
                            date = patstory.getDate(sc)
                            print 'date: ', date
                            print 'time: ', mp3_dict['mp3_time']
                            print 'mp3_path: ', mp3_dict['mp3_path']
                            print 'lrc_path: ', lrc_path
                            pic_path = patstory.getPicture(sc, jpg_path, png_path, default_path)
                            print 'pic_path: ', pic_path
                            print 'audioPartEndTime: ', content_dict['audioPartEndTime']
                            audioTextBlank_dict = patstory.dig_word(content_dict['content'])
                            print 'audioTextBlankIndex: ', audioTextBlank_dict['audioTextBlankIndex']
                            print 'audioTextBlankWord: ', audioTextBlank_dict['audioTextBlankWord']
                            print 'content: ', content_dict['content']
                            id = id + 1

                            #   在这里写存库的语句

        return id


if __name__ == '__main__':
    a = PatVoA()
    a.getArticle()