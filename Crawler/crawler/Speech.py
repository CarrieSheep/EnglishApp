__author__ = 'carrie'
#coding=utf-8

from K_Method import GetUrlMethod, PatStoryMethod
import chardet
from urllib import urlopen
import re

class PatSpeach():

     #爬取网页链接
    def getUrl(self):
        startUrl_list = ['http://www.kekenet.com/Article/kkspeech/weekztyj/', 'http://www.kekenet.com/Article/15206/',
                     'http://www.kekenet.com/Article/15297/']
        fnum_list = [57, 1, 0]
        lnum_list = [65, 3, 0]
        page_list = []
        method = GetUrlMethod()
        # 获取网页url
        for index in range(0, len(startUrl_list)):
            page_url = method.getPageUrl(fnum_list[index], lnum_list[index], startUrl_list[index])
            for url in page_url:
                page_list.append(url)
        #获取每篇演讲的url,MP3下载地址,标题
        dict = method.getStoryAndMP3UrlAndTitle(page_list, 'Article')
        return dict


    def getArticle(self, id):
        dict = self.getUrl()
        speech_list = dict['story']
        mp3_list = dict['mp3']
        title_list = dict['title']
        print len(title_list)
        num = 0
        for index in range(0, len(speech_list)):
            url = speech_list[index]
            patstory = PatStoryMethod()
            sc = patstory.getStorySC(url)
            lrc = r'/home/carrie/downloads/kekenet-speech/lrc/' + str(index) + r'.lrc' # 需更改路径
            mp3 = r'/home/carrie/downloads/kekenet-speech/mp3/' + str(index) + r'.mp3' # 需更改路径
            jpg_path = '/home/carrie/downloads/kekenet_speech/picture/' +str(index) + '.jpg'# 需更改路径
            png_path = '/home/carrie/downloads/kekenet_speech/picture/' + str(index) + '.png'# 需更改路径
            default_path = '/home/carrie/downloads/kekenet_speech/picture/default.jpg'
            lrc_path = patstory.getLrc(mp3_list[index], lrc)
            if lrc_path != '':
                #判断文本是否有中文翻译
                text = urlopen(lrc_path).read()
                c = chardet.detect(text)
                code = c['encoding']
                text = str(text).decode(code, 'ignore').encode('utf-8').replace('\n', '')
                text = text.decode('utf-8')
                a = re.findall(u'[\u4e00-\u9fa5]', text)
                if len(a) >= 100:
                    mp3_dict = patstory.getMP3AndTime(mp3_list[index], mp3)
                    if mp3_dict['mp3_time'] <= 300:
                        total_time = mp3_dict['mp3_time'] * 1000
                        content_dict = patstory.getContent(lrc_path, total_time)
                        if content_dict['content'] != '':
                            print 'id: ',id
                            type = 'speech'
                            print 'type: ', type
                            title = title_list[index]
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
    a = PatSpeach()
    a.getArticle()
#公众人物演讲  1-15
#希拉里演讲   1-2
#乔布斯演讲   1
#facebook   1
#TED十佳演讲    1-14
#百度李宏彦  1
#twitter  1
#哈佛大学经典演讲  1-3