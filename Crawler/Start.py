__author__ = 'carrie'
#coding=utf-8
import re
from urllib import urlopen,urlretrieve

class GetUrlMethod():

    #爬取页面链接
    def getPageUrl(self,num, startUrl):
        page_list = []
        for i in range(1, num):
            http = startUrl +'List_' + str(i) + '.shtml'
            page_list.append(http)
        page_list.append(startUrl)
        # print 1, page_list
        return page_list

    #获取每个故事的链接
    def getStoryAndMP3UrlAndTitle(self,page_list,type):
        story_list = []
        mp3_list = []
        title_list = []
        for page in page_list:
            text = urlopen(page).read()
            text = str(text).replace('\r\n', '')
            pattern= re.compile('http://www.kekenet.com/' + type + '/2.*?target')
            pattern_url = re.compile('http://www.kekenet.com/' + type + '/2.*?shtml')
            pattern_title = re.compile(r'《.*?target')
            ulist = []
            tlist = []
            b = re.findall(pattern, text)
            for item in b:
                ulist.append(re.findall(pattern_url, item)[0])
                title = re.findall(pattern_title, item)
                tlist.append(re.sub(r'" target', '', title[0]))
            for index in range(0,len(ulist)):
                #获取MP3下载地址链接,查看MP3是否存在,若不存在,则该是链接不存储
                mp3_url = ulist[index].replace(type, 'mp3')
                text = urlopen(mp3_url).read()
                a = re.search(r'http://xia.*?mp3', text)
                if a != None:
                    story_list.append(ulist[index])
                    mp3_list.append(a.group())
                    title_list.append(tlist[index])
        dict = {'story': story_list, 'mp3': mp3_list, 'title': title_list}
        # print 3, story_list
        # print 3, mp3_list
        return dict


class PatStoryMethod():

    #爬取故事的源代码
    def getStorySC(self,url):
        text = urlopen(url).read()
        sc = str(text)
        sc = re.sub(r'\n', '', sc)
        # print 4, sc
        return sc

     #爬取每个故事的内容
    def getContent(self, sc):
        a = re.compile('<div class="qh_.*?</div>')
        article = re.findall(a, sc)
        content_zg = []
        content_en = []
        if article == []:
            article = re.findall(r'<span id="article_eng">.*?<script>', sc)[0]
            if article !=[]:
                a = re.sub(r'<BR></FONT>', '@@@@', article)
                a = re.sub(r'<BR><FONT.*?>', '@@@@', a)
                a = re.sub(r'</FONT> <BR>', '@@@@', a)
                a = re.sub(r'<BR></STRONG></FONT>', '@@@@', a)
                a = re.sub(r'<P><FONT.*?>', '@@@@', a)
                a = re.sub(r'<br />', '@@@@', a)
                a = re.sub(r'<.*?>', '', a)
                article = re.split('@@@@', a)
            else:
                article = []
        if len(article) > 5:
            num = 0
            for item in article:
                item = re.sub(r'<.*?>', '', item).replace('&#39;', "'").replace('&quot;', '"')
                item = item.replace('&ldquo;', '"').replace('&rdquo;', '"').replace('&bull;', '·')
                item = item.replace('&hellip;', '…').replace('&middot;','·')
                if len(item) > 0:
                    if num%2 == 0:
                        content_en.append(item)
                    else:
                        content_zg.append(item)
                    num = num + 1
            content_dict = {'en': content_en, 'zg': content_zg}
        else:
            content_dict = {}
        return content_dict

    # def getTitle(self,content):
    #     title = re.split('\r\n', content)
    #     title = title[0]
        # print 6, title
        # return title

    #爬取每个故事的音频
    def getMP3(self, mp3, index, storeAdd):
        mp3_path = r'/home/carrie/downloads/' + storeAdd + '/mp3/' + storeAdd + str(index) + r'.mp3'
        urlretrieve(mp3, mp3_path)
        return mp3_path

    #爬取每个故事的图片
    def getPicture(self, sc, index, storeAdd,pic):
        pic_url = re.search(r'http://pic.kekenet.*?jpg', sc)
        if pic_url != None:
            pic_url = pic_url.group()
            if len(pic_url) > 100:
                a = re.findall(r'http://pic.kekenet.*?jpeg', pic_url)
                if a == []:
                    b = re.findall(r'http://pic.kekenet.*?JPG', pic_url)
                    if b == []:
                        pic_url =re.findall(r'http://pic.kekenet.*?png', pic_url)[0]
                    else:
                        pic_url = b[0]
                else:
                    pic_url = a[0]
        else:
            pic_url = pic

        if re.findall('png', pic_url) == []:
            pic_path = r'/home/carrie/downloads/'+storeAdd+'/picture/' + storeAdd +str(index) + r'.jpg'
            urlretrieve(pic_url, pic_path)
        else:
            pic_path = r'/home/carrie/downloads/'+ storeAdd+ '/picture/' + storeAdd + str(index) + r'.png'
            urlretrieve(pic_url, pic_path)
        return pic_path

    #爬取音频上传时间
    def getDate(self, sc):
        date = re.findall(r'<time.*?time>',sc)
        date = re.findall(r':(.*?)</time',date[0])
        date = date[0]
        # print date
        return date