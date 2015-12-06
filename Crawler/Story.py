#coding = utf-8
__author__ = 'carrie'
import re
import chardet
from urllib import urlopen,urlretrieve

class PatStory():


    def getPageUrl(self):
        page_list = []
        page_list.append('http://www.kekenet.com/menu/13407/')
        for i in range(34,34):
            http = 'http://www.kekenet.com/menu/13407/List_%s' % i + '.shtml'
            # print http
            page_list.append(http)
        print 1, page_list
        return page_list


    def getStoryUrl(self):
        story_list = []
        page_list = self.getPageUrl()
        # print 2, page_list
        for page in page_list:
            text = urlopen(page).read()
            text = str(text).replace('\r\n','')
            b = re.compile(r'http://www.kekenet.com/menu/2.*?shtml')
            list = re.findall(b, text)
            # print 3, list
            for story in list:
                story_list.append(story)
        print 4, story_list
        return story_list


    def getStorySC(self):
        sc_list = []
        story_list = self.getStoryUrl()
        for story in story_list:
            text = urlopen(story).read()
            text = str(text).replace('\r\n', '')
            sc_list.append(text)
        # print 5, sc_list
        return sc_list


    def getContentAndTitle(self):
        content_list = []
        title_list = []
        sc_list = self.getStorySC()
        for content in sc_list:
            a = re.compile(r'<div class="qh_.*?</div>')
            article = re.findall(a, content)
            essay = ''
            title = ''
            count = 0
            for item in article:
                item = re.sub(r'<.*?>', '', item).replace('&#39;', "'")
                # print item
                if count < 2:
                    title = title + item + '  '
                    count += 1
                essay = essay + '\r\n' + item
            content_list.append(essay)
        contentAndTitle_dict = {'content':content_list,'title':title_list}
        print 6, contentAndTitle_dict
        return contentAndTitle_dict


    def getMP3Url(self):
        mp3_list = []
        mp3Url_list = []
        story_list = self.getStoryUrl()
        for story in story_list:
            mp3_dowmload = story.replace('menu','mp3')
            # print mp3_dowmload
            text = urlopen(mp3_dowmload).read()
            a = re.search(r'http://xia.*?mp3', text)
            # print a
            if a == None:
                mp3Url_list.append('')
            else:
                mp3Url_list.append(a.group())
        print 7, mp3Url_list
        return mp3Url_list


    def getMP3(self):
        i = 0
        mp3Url_list = self.getMP3Url()
        for mp3 in mp3Url_list:
            if mp3 != []:
                a = r'/home/carrie/downloads/story/mp3/' + str(i) + r'.mp3'
                urlretrieve(mp3,a)
            i += 1


    def getPictureUrl(self):
        sc_list = []
        picture_list = []
        for sc in sc_list:
            pic_download = re.search(r'http://pic.kekenet.*?jpg', sc)
            if pic_download != None:
                pic_download = pic_download.group()
                if len(pic_download) > 100:
                    a = re.findall(r'http://pic.kekenet.*?jpeg', pic_download)
                    if a == []:
                        b = re.findall(r'http://pic.kekenet.*?JPG', pic_download)
                        if b == []:
                            pic_download =re.findall(r'http://pic.kekenet.*?png',pic_download)[0]
                        else:
                            pic_download = b[0]
                    else:
                        pic_download = a[0]
            else:
                pic_download = ''
            print 8, pic_download
            picture_list.append(pic_download)
        return picture_list


    def getPicture(self):
        i = 0
        picture_list = self.getPictureUrl()
        for picture in picture_list:
            if picture != '':
                if re.findall('png',picture) == []:
                    a = r'/home/carrie/downloads/story/picture/' + str(i) + r'.jpg'
                    urlretrieve(picture,a)
                else:
                    a = r'/home/carrie/downloads/story/picture/' + str(i) + r'.png'
                    urlretrieve(picture,a)
            i += 1


if __name__ == '__main__':
    a = PatStory()
    # a.getStoryUrl()
    a.getContentAndTitle()
    a.getMP3()
    a.getPicture()