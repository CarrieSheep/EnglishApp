__author__ = 'carrie'
#coding=utf-8

from Start import GetUrlMethod, PatStoryMethod

class PatMaritimePianist():

     #爬取网页链接
    def getPageUrl(self):
        startUrl = 'http://www.kekenet.com/video/movie/piano/'
        method = GetUrlMethod()
        page_list = method.getPageUrl(3, startUrl)
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
                mp3_path = patstory.getMP3(mp3_list[index], index, 'MaritimePianist')
                print 3, mp3_path
                pic = "http://pic.kekenet.com/2012/0223/20120223034042496.jpg"
                pic_path = patstory.getPicture(sc, index, 'MaritimePianist', pic)
                print 4, pic_path
                for i in range(0,len(content_dict['en'])):
                    print 5, content_dict['en'][i]
                    print 6,content_dict['zg'][i]




if __name__ == '__main__':
    a = PatMaritimePianist()
    a.getArticle()
