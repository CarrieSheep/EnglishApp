__author__ = 'carrie'
#coding=utf-8

from Start import GetUrlMethod,PatStoryMethod

#泰坦尼克号电影片段
class PatTitanicUrl():

    #爬取网页链接
    def getPageUrl(self):
        startUrl = 'http://www.kekenet.com/menu/13465/'
        method = GetUrlMethod()
        page_list = method.getPageUrl(5, startUrl)
        # print 1,page_list
        return page_list

    def getStoryAndMp3UrlAndTitle(self):
        page_list = self.getPageUrl()
        method = GetUrlMethod()
        dict = method.getStoryAndMP3UrlAndTitle(page_list, 'menu')
        # story_list = dict['story']
        # mp3_list = dict['mp3']
        # title_list = dict['title']
        # print 3, len(story_list),story_list
        # print 3, len(mp3_list),mp3_list
        # print 3, len(title_list),title_list
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
                mp3_dict = patstory.getMP3AndTime(mp3_list[index], index, 'Titanic')
                print 3, mp3_dict['mp3_time']
                print 4, mp3_dict['mp3_path']
                pic = 'http://pic.kekenet.com/2013/0203/5551359887061.jpg'
                pic_path = patstory.getPicture(sc, index, 'Titanic', pic)
                print 5, pic_path
                for i in range(0, len(content_dict['en'])):
                    print 6, content_dict['en'][i]
                    if i < len(content_dict['zg']):
                        print 7, content_dict['zg'][i]
                print '\n'

if __name__ == '__main__':
    a = PatTitanicUrl()
    a.getArticle()



