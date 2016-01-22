__author__ = 'carrie'
#coding=utf-8
import re
from urllib import urlopen, urlretrieve
import eyed3
import chardet
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import random

class GetUrlMethod():

    #爬取页面链接
    def getPageUrl(self, fnum, lnum, startUrl):
        page_list = []
        for i in range(fnum, lnum):
            http = startUrl + 'List_' + str(i) + '.shtml'
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
            # print page
            text = urlopen(page).read()
            # print text
            text = str(text).replace('\r\n', '')
            # print text
            pattern= re.compile('http://www.kekenet.com/' + type + '/2.*?target')
            pattern_url = re.compile('http://www.kekenet.com/' + type + '/2.*?shtml')
            pattern_title = re.compile(r'="(.*?)" target')
            ulist = []
            tlist = []
            b = re.findall(pattern, text)
            for item in b:
                # print item
                ulist.append(re.findall(pattern_url, item)[0])
                title = re.findall(pattern_title, item)
                # print title
                tlist.append(re.sub(r'(MP3\+中英字幕)', '', title[0]).replace('()',''))
                # tlist.append(title[0])
            for index in range(0,len(ulist)):
                #获取MP3下载地址链接,查看MP3是否存在,若不存在,则该是链接不存储
                mp3_url = ulist[index].replace(type, 'mp3')
                text = urlopen(mp3_url).read()
                a = re.search(r'http://xia.*?mp3', text)
                if a != None:
                    # print ulist[index]
                    # print tlist[index]
                    story_list.append(ulist[index])
                    mp3_list.append(a.group())
                    title_list.append(tlist[index])
        dict = {'story': story_list, 'mp3': mp3_list, 'title': title_list}
        return dict


class PatStoryMethod():

    #爬取故事的源代码
    def getStorySC(self, url):
        text = urlopen(url).read()
        sc = str(text)
        sc = re.sub(r'\n', '', sc)
        # print 4, sc
        return sc

    #获取lrc文件
    def getLrc(self, mp3_url, lrc):
        b = re.compile('http.*?com/')
        mp3_pattern = re.sub(b, '', mp3_url)
        lrc_url = 'http://www.kekenet.com/' + mp3_pattern + '.lrc'
        text = urlopen(lrc_url).read()
        text = str(text)
        text = re.sub(r'\n', '', text)
        a = re.findall(r'\[.*?\]', text)
        if len(a) >= 5:
            lrc_path = lrc
            urlretrieve(lrc_url, lrc_path)
            return lrc_path
        else:
            return ''

    def getTitle(self, title):
        title = re.sub('\(.*?\)','',title)
        return title

     #爬取每个故事的内容

    #获取文章分割点
    def getCut(self, lrc, total_time):
        list1 = re.findall('\[[0-9\.:]+]',lrc)
        time_chok=[]
        actual_time=[]
        # print list1
        for i in list1:
            if i !='':
                a=re.findall('\[(.*?):',i)
                b=re.findall(':(.*?)]',i)
                min=int(a[0])
                second=float(b[0])
                time_chok.append((min, second))
                actual_time.append((min*60+second)*1000)
        # print time_chok
        # print actual_time
        first = second = first_chok = second_chok = 0
        for i in range(len(actual_time)) :
            if actual_time [i]>total_time /3:
                first=actual_time [i-1]
                first_chok= i-1
                break
        for i in range(len(actual_time)) :
            if actual_time[i]>total_time /3*2:
                second=actual_time[i-1]
                second_chok = i-1
                break
        # print first, second
        # print first_chok, second_chok, time_chok[first_chok], time_chok[second_chok ]
        #判断音频长度与lrc长度相等
        if (first!= 0)and (second!=0):
            dict = {'first_index': first_chok, 'second_index': second_chok, 'first_time': first, 'second_time': second}
            return dict
        else:
            return ''

    def getContent(self, lrc_path, total_time):
        # print total_time
        text = urlopen(lrc_path).read()
        c = chardet.detect(text)
        code = c['encoding']
        text = str(text).decode(code, 'ignore').encode('utf-8').replace('\r\n', '')
        # print text
        #删除无用内容
        text = re.sub('\[by:.*?com\]','',text).replace(r'\[ti:]','').replace(r'[ar:]','').replace(r'[al:]','')
        # print text
        #将文章按句分开
        content_list = re.split(r'\[.*?\]', text)
        pattern_zg = re.compile(u'[\u4e00-\u9fa5]')
        pattern_en = re.compile(u'(.*?)\(*[a-zA-Z]*"*-*《*“*\d*[\u4e00-\u9fa5]')
        content = ''
        count = 0
        num = 0
        dict = self.getCut(text, total_time)
        if dict != '':
            first_index = dict['first_index']
            second_index = dict['second_index']
            first_time = dict['first_time']
            second_time = dict['second_time']
            for item in content_list:
                if item != '':
                    # print item
                    text = item.decode('utf-8')
                    if re.findall(pattern_zg, text) != []:
                        en = re.findall(pattern_en, text)[0]
                        zg = text.replace(en, '')
                        content = content + en + u'##' + zg + u'##'
                    else:
                        count = count + 1
                        content = content + item + u'####'
                    if (num == (first_index - 1)) or (num == (second_index - 1)):
                        content = content + u'$$'
                    num = num + 1
            audioPartEndTime = str(first_time) + '##' + str(second_time) + '##' + str(total_time)
            #判断没有中文解释的句子是否超过10条
            if count >= 10:
                content_dict = {'content':'', 'audioPartEndTime': audioPartEndTime}
                return content_dict
            else:
                content = content.encode('utf-8')
                content_dict = {'content':content, 'audioPartEndTime': audioPartEndTime}
                return content_dict
        else:
            content_dict = {'content':'', 'audioPartEndTime': ''}
            return content_dict

    #爬取每个故事的音频
    def getMP3AndTime(self, mp3_url, path):
        mp3_path = path
        # urlretrieve(mp3_url, mp3_path)
        audio = eyed3.load(mp3_path)
        mp3_time = audio.info.time_secs
        # sec = mp3_time % 60
        # min = mp3_time / 60g
        # mp3_time = str(min) + ':' + str(sec)
        mp3_dict = {'mp3_path': mp3_path, 'mp3_time': mp3_time}
        return mp3_dict

    #爬取每个故事的图片
    def getPicture(self, sc, jpg_path, png_path,default_path):
        pic_url = re.search(r'http://pic.kekenet.*?jpg', sc)
        pic_path = default_path
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
            if re.findall('png', pic_url) == []:
                pic_path = jpg_path
                urlretrieve(pic_url, pic_path)
            else:
                pic_path = png_path
                urlretrieve(pic_url, pic_path)
        return pic_path

    #爬取音频上传时间
    def getDate(self, sc):
        date = re.findall(r'<time.*?time>',sc)
        date = re.findall(r':(.*?)</time',date[0])
        date = date[0]
        # print date
        return date

    # 获取六级单词
    def get_six_word(self):
        f2 = open('/home/carrie/EnglishApp/Crawler/6级单词.txt','r')
        list2 = f2.readlines()
        six_word_dict=[]
        for i in list2:
            word = re.search('[a-z].*? ',i)
            if word:
                six_word_dict .append(word.group())
        return six_word_dict

    #获取挖空词的下标
    def dig_word(self, content):
        part = content.split("$$")
        english_part = [[], [], []]
        mix_part = []
        stopset = set(stopwords.words('english'))#停止词词库数组
        stemmer=SnowballStemmer('english')
        six_word = self.get_six_word()
        root = []#这个是6级所有单词的词根
        for i in range(len(six_word)):
            root.append(stemmer.stem(six_word [i].strip()))
        for i in range(len(part)) :
            # print part[i]
            mix_part .append(part[i].split("##"))
        # print mix_part
            for j in range(len(mix_part[i])) :
                if j%2==0 and mix_part[i][j]!='':
                    english_part[i].append(mix_part[i][j] )
                    # print mix_part[i][j]
        paragraph=[]
        for i in english_part :
            a=''
            for j in i:
               a+=j
            paragraph.append(a)
        for i in paragraph :
            print i
        pattern=r' *([a-zA-Z\'-]+)'
        head_len=[]
        head_index=[]
        head_answer=[]
        audioTextBlankIndex = ''
        audioTextBlankWord = ''
        for z in range(3):
            all_word_list = re.findall(pattern, paragraph[z])
            # print all_word_list
            # print len(all_word_list)
            head_len .append(len(all_word_list))
            withoutstop_list = []
            same=[]
            stem_word=[]
            index=[]
            answer=[]
            amount=len(all_word_list)/10

            for i in range(len(all_word_list)) :
                all_word_list [i]=all_word_list [i].lower()
                stem_word.append(stemmer.stem(all_word_list[i] ))
                if all_word_list[i] not in stopset :
                    withoutstop_list .append(all_word_list [i])
            # for i in withoutstop_list :
            #     print i

            for i in stem_word :
                if i in root:
                    if i not in same:
                        if len(same)<amount:
                            same.append(i)
            # print len(same), same
            for i in same:
                index.append(stem_word.index(i))
            if len(index) < amount:
                a = range(0, len(all_word_list))
                random.shuffle(a)
                # for i in range(amount-len(index)):
                for i in a:
                    if len(index) >= amount:
                        break
                    if i not in index:
                        index.append(i)
            index = sorted(index)
            head_index .append(index)
            # print len(index),index
            for i in index:
                answer .append(all_word_list[i])
                audioTextBlankWord = audioTextBlankWord + all_word_list[i] + '##'
            audioTextBlankWord = audioTextBlankWord + '$$'
            # print answer
            head_answer.append(answer)
        # print head_index
        # print head_answer
        # print head_len
        index=[]
        for i in range(len(head_index)):
            if (i==1) or (i==2):
                audioTextBlankIndex = audioTextBlankIndex + '$$'
            for j in range(len(head_index[i])):
                if i ==0:
                    num = head_index[i][j]
                    index.append(num)
                if i==1:
                    num = head_index[i][j]+head_len[0]
                    index.append(num)
                if i==2:
                    num = head_index[i][j]+head_len[0]+head_len[1]
                    index.append(num)
                audioTextBlankIndex = audioTextBlankIndex + str(num) + '##'
        # print index
        dict = {'audioTextBlankIndex': audioTextBlankIndex, 'audioTextBlankWord': audioTextBlankWord}
        return dict
