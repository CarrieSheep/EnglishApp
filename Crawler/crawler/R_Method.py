__author__ = 'carrie'
#coding=utf-8
import re
from urllib import urlopen, urlretrieve
import chardet
import eyed3
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import random


class Method():

    # 进行解码和编码方法
    def getCode(self, url):
        text = urlopen(url).read()
        c = chardet.detect(text)
        code = c['encoding']
        text = str(text).decode(code, 'ignore').encode('utf-8').replace('\r\n', '')
        return text

    # 爬取网页链接
    def getPageUrl(self, url):
        text = self.getCode(url)
        #获取包含电影链接的代码段
        pattern_code = re.compile(r'<div class="lmflbot bg">.*?</div>')
        url_code = re.findall(pattern_code, text)
        # print 'url_code:', url_code[0]
        pattern_url = re.compile(r'<a href="(.*?)" Title')
        url_list = re.findall(pattern_url, url_code[0])
        return url_list

    #获取故事链接
    def getMovieUrlAndTitle(self, url):
        text = self.getCode(url)
        #爬取包含链接和标题的代码段
        pattern_code = re.compile(r'<div class="lm2flbot2">.*?</div>')
        url_code = re.findall(pattern_code, text)
        #爬取图片链接
        pic_code = re.findall(r'src="/English/Files/.*?jpg"', text)
        pic_url = ''
        if len(pic_code)> 0:
            pic_url = re.findall(r'"(.*?)"', pic_code[0])[0]
        #爬取链接
        pattern_url = re.compile(r'<a href="(.*?)" Title')
        url_list = re.findall(pattern_url, url_code[0])
        #爬取标题
        pattern_title = re.compile(r'Title="(.*?)" target')
        title_list = re.findall(pattern_title, url_code[0])
        dict = {'title': title_list, 'url': url_list, 'pic_url': pic_url}
        return dict

    #爬取mp3和lrc的链接
    def getMP3AndLrcUrl(self, url):
        text = self.getCode(url)
        mp3 = re.findall(r"var mp3url = '(.*?)'", text)[0]
        lrc = re.findall(r"var texturl ='(.*?)'", text)[0]
        dict = {'mp3': mp3, 'lrc': lrc}
        return dict

    # 标题简化
    def getTitle(self, title):
        pattern_1 = u'听电影MP3学英语之'
        pattern_2 = u'附中英双语LRC字幕和文本'
        pattern_3 = u' 中英双语MP3+LRC+文本'
        pattern_4 = u'中英双语MP3+LRC'
        pattern_5 = u' 原版MP3+中英LRC字幕'
        pattern_6 = u'听电影MP3学英语 '
        pattern_7 = u'MP3+中英文LRC字幕'
        pattern_8 = u'BBC迷你剧'
        pattern_9 = u'电影Mp3对白学英语'
        title = title.decode('utf-8')
        title = re.sub(pattern_4,'',title).replace(pattern_5,'').replace(pattern_6,'').replace(pattern_7,'')
        title = re.sub(pattern_1,'',title).replace(pattern_2,'').replace(pattern_3,'').replace(pattern_8,'')
        title = re.sub(pattern_9,'',title)
        return title.encode('utf-8')

    def getMP3(self, index, url):
        mp3_path = r'/home/carrie/downloads/rrting/mp3/' + str(index) + '.mp3' # 需更改存储路径
        urlretrieve(url, mp3_path)
        audio = eyed3.load(mp3_path)
        time = audio.info.time_secs   #获取音频时长
        dict = {'path': mp3_path, 'time': time}
        return dict

    def getLrc(self, index, url):
        lrc_path = r'/home/carrie/downloads/rrting/lrc/' + str(index) + '.lrc'  #需更改存储路径
        urlretrieve(url, lrc_path)
        return lrc_path

    def getPicture(self, index, start, url):
        if url == '':
            pic_path = '/home/carrie/downloads/rrting/picture/default.jpg' #默认的图片， 需更改路径
            return pic_path
        else:
            if index == start:  # 第一次爬取该电影的片段，需下载图片
                pic_path = '/home/carrie/downloads/rrting/picture/' + str(start) + '.jpg' #需更改路径
                urlretrieve(url, pic_path)
                return pic_path
            else: #不是第一次下载该电影的片段，直接调用第一次下载该电影的片段时下载的图片
                pic_path = '/home/carrie/downloads/rrting/picture/' + str(start) + '.jpg'
                return pic_path

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
        if (first!= 0)and (second!=0):  #音频长度与lrc文本长度相同，返回以下属性
            dict = {'first_index': first_chok, 'second_index': second_chok, 'first_time': first, 'second_time': second}
            return dict
        else: # 音频长度与lrc文本长度相差较大时，返回空字符串
            return ''

    def getContent(self, lrc_path, total_time):
        text = self.getCode(lrc_path)
        # print text
        #删除无用内容
        text = re.sub('\[00:00.00.*?mp3/', '', text)
        text = re.sub('\[00:00.01.*?hand', '', text).replace('◎', '').replace('- ', '')
        # print text
        #将文章按句分开
        content_list = re.split(r'\[.*?\]', text)
        pattern_zg = re.compile(u'[\u4e00-\u9fa5]')
        pattern_en = re.compile(u'(.*?)[\("-《“a-zA-Z]*\d*[\u4e00-\u9fa5]')
        content = ''
        count = 0
        num = 0 # 计算文本的句数
        dict = self.getCut(text, total_time)
        if dict != '': # 音频长度与lrc文本长度相同
            first_index = dict['first_index'] # 音频分割第一次分割点--句的下标
            second_index = dict['second_index'] # 音频第二次分割点--句的下标
            first_time = dict['first_time']  #音频第一次分割的时间戳
            second_time = dict['second_time'] #音频第二次分割的时间戳
            for item in content_list:
                if item != '':
                    # print item
                    text = item.decode('utf-8') #转换成unicode编码
                    if re.findall(pattern_zg, text) != []: # 文本含有中文
                        en = re.findall(pattern_en, text)[0] # 匹配出该句中的英文
                        zg = text.replace(en, '') # 匹配出该句中的英文
                        content = content + en + u'##' + zg + u'##'
                    else:
                        count = count + 1
                        content = content + item + u'####'
                    if (num == (first_index - 1)) or (num == (second_index - 1)): # 在分割点的前一句的末尾插入两个美元符号
                        content = content + u'$$'
                    num = num + 1
            audioPartEndTime = str(first_time) + '##' + str(second_time) + '##' + str(total_time)
            if count >= 20: #不含有中文翻译或较多语气词的文本，删除文本
                content_dict = {'content': '', 'audioPartEndTime': audioPartEndTime}
                return content_dict
            else:
                content = content.encode('utf-8')
                content_dict = {'content':content, 'audioPartEndTime': audioPartEndTime}
                return content_dict
        else:
            content_dict = {'content':'', 'audioPartEndTime': ''}
            return content_dict

    # 获取六级单词
    def get_six_word(self):
        f2 = open('/home/carrie/EnglishApp/Crawler/6级单词.txt','r')  # 需更改路径
        list2 = f2.readlines()
        six_word_dict=[]
        for i in list2:
            word = re.search('[a-z].*? ', i)
            if word:
                six_word_dict .append(word.group())
        return six_word_dict



    def getDate(self, url):
        text = self.getCode(url)
        date = re.findall(r'<div id="N_small"><span>.*?</span>', text)[0]
        date = re.sub(r'<div id="N_small">.*?:', '', date)
        date = re.sub(r'</span>', '', date)
        return date

    def getArticle(self,index, start, total_time, title, mp3_path, lrc_url, pic_url, url, id):
        lrc_path = self.getLrc(index, lrc_url)
        content_dict = self.getContent(lrc_path, total_time)
        if content_dict['content'] != '':
            print 'id: ', id
            title = self.getTitle(title)
            print 'title: ', title
            date = self.getDate(url)
            type = 'movie'
            print 'type: ', type
            print 'date: ', date
            print 'mp3_path: ', mp3_path
            print 'lrc_path: ', lrc_path
            pic_url = self.getPicture(index, start, pic_url)
            print pic_url
            print 'audioPartEndTime: ', content_dict['audioPartEndTime']
            audioTextBlank_dict = self.dig_word(content_dict['content'])
            print 'audioTextBlankIndex: ', audioTextBlank_dict['audioTextBlankIndex']
            print 'audioTextBlankWord: ', audioTextBlank_dict['audioTextBlankWord']
            print 'content: ', content_dict['content']
            id = id + 1

            #   在这里写存库的语句

        return id

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
        # for i in paragraph :
            # print i
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




