#coding=utf-8
__author__ = 'carrie'

import re
from urllib import urlopen,urlretrieve


class PatStoryUrl():

    #获取网页链接
    def getPageUrl(self):
        page_list = []
        for i in range(1,1):
            http = 'http://www.kekenet.com/menu/13407/List_%s' % i + '.shtml'
            page_list.append(http)
        page_list.append('http://www.kekenet.com/menu/13407/')
        # print 1, page_list
        return page_list

    #获取每个故事的链接
    def getStoryAndMP3Url(self):
        story_list = []
        mp3_list = []
        page_list = self.getPageUrl()
        for page in page_list:
            text = urlopen(page).read()
            text = str(text).replace('\r\n','')
            b = re.compile(r'http://www.kekenet.com/menu/2.*?shtml')
            list = re.findall(b, text)
            # print 2, list
            for story in list:
                mp3_url = story.replace('menu', 'mp3')
                text = urlopen(mp3_url).read()
                a = re.search(r'http://xia.*?mp3', text)
                if a != None:
                    story_list.append(story)
                    mp3_list.append(a.group())
        dict = {'story':story_list,'mp3':mp3_list}
        # print 3, story_list
        # print 3, mp3_list
        return dict

#爬取每个故事的标题,内容,音频和图片
class PatStory():

    #爬取故事的源代码
    def getStorySC(self):
        text = urlopen(url).read()
        sc = str(text).replace('\r\n', '')
        # print 4, sc
        return sc

    #爬取每个故事的内容
    def getContent(self):
        a = re.compile('<div class="qh_.*?</div>')
        article = re.findall(a, sc)
        content = ''
        if article != []:
            for item in article:
                item = re.sub(r'<.*?>', '', item).replace('&#39;', "'").replace('&quot;', '"')
                content = content + item + '\r\n'
        else:
            content = ''
        print 5, content
        return content

    #爬取每个故事的标题
    def getTitle(self):
        title = re.split('\r\n',content)
        title = title[0]
        print 6, title
        return title

    #爬取每个故事的音频
    def getMP3(self):
        a = r'/home/carrie/downloads/story/mp3/' + str(i) + r'.mp3'
        urlretrieve(mp3, a)

    #爬取每个故事的图片
    def getPicture(self):
        pic_url = re.search(r'http://pic.kekenet.*?jpg', sc)
        if pic_url != None:
            pic_url = pic_url.group()
            if len(pic_url) > 100:
                a = re.findall(r'http://pic.kekenet.*?jpeg', pic_url)
                if a == []:
                    b = re.findall(r'http://pic.kekenet.*?JPG', pic_url)
                    if b == []:
                        pic_url =re.findall(r'http://pic.kekenet.*?png',pic_url)[0]
                    else:
                        pic_url = b[0]
                else:
                    pic_url = a[0]
            if re.findall('png', pic_url) == []:
                a = r'/home/carrie/downloads/story/picture/' + str(i) + r'.jpg'
                urlretrieve(pic_url, a)
            else:
                a = r'/home/carrie/downloads/story/picture/' + str(i) + r'.png'
                urlretrieve(pic_url, a)

    #爬取每个故事的lrc文件
    def getLrc(self):
        lrc = mp3.replace('xia2','www')
        lrc = lrc + '.lrc'
        print lrc
        a = r'/home/carrie/downloads/story/lrc/' + str(i) + r'.lrc'
        urlretrieve(lrc, a)

if __name__ == '__main__':
    a = PatStoryUrl()
    story_list = a.getStoryAndMP3Url()['story']
    mp3_list = a.getStoryAndMP3Url()['mp3']
    for i in range(0,len(story_list)):
        url = story_list[i]
        b = PatStory()
        sc = b.getStorySC()
        content = b.getContent()
        if content != '':
            b.getTitle()
            mp3 = mp3_list[i]
            # print mp3
            b.getMP3()
            b.getPicture()
            b.getLrc()









