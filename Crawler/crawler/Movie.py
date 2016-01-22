__author__ = 'carrie'
#coding=utf-8

from R_Method import Method
import chardet
from urllib import urlopen
import re

class PatMovie():

    def getArticle(self, id):
        a = Method()
        url_list = a.getPageUrl('http://www.rrting.net/English/movie_mp3/')
        title_list = []
        movie_list = []
        pic_list = []
        start_list = [0] # 设置列表start_list:存储每部电影第一个片段在movie_list的下标,目的：减少相同图片的下载
        count = 0
        # print url_list
        for index in range(1, 15):
            url = 'http://www.rrting.net' + url_list[index]
            dict = a.getMovieUrlAndTitle(url)
            title_list = title_list + dict['title']
            movie_list = movie_list + dict['url']
            for index in range(0,len(dict['url'])):
                pic_list.append(dict['pic_url'])
            count = count + len(dict['url'])
            start_list.append(count)
            # print dict['title'][0]
        count = 0 # 计算爬虫已经爬取到哪部电影
        # print start_list
        start = start_list[count]
        for index in range(11, 200):
            url = 'http://www.rrting.net' + movie_list[index] + 'mp3para.js' # 下载MP3和lrc的网址
            movie_url = 'http://www.rrting.net' + movie_list[index]
            dict_url = a.getMP3AndLrcUrl(url)
            mp3_url = dict_url['mp3']
            # print mp3_url
            mp3_info = a.getMP3(index, mp3_url)
            time = mp3_info['time']
            if time <= 300:
                total_time = time * 1000
                if pic_list[index] != '': # 该电影片段存在图片链接，传入图片下载地址
                    pic_url = 'http://www.rrting.net' + pic_list[index]
                else: # 该电影片段不存在图片，传入空字符串
                    pic_url = ''
                if index >= start_list[count + 1]: # 爬虫开始爬取下一部电影的片段，切换图片
                    count = count+1
                    start = start_list[count]
                id = a.getArticle(index, start, total_time, title_list[index], mp3_info['path'], dict_url['lrc'],
                             pic_url, movie_url, id)
        return id


if __name__ == '__main__':
    a = PatMovie()
    a.getArticle()