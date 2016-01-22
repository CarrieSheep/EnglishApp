__author__ = 'carrie'
#coding=utf-8
from Movie import PatMovie
from Speech import PatSpeach
from VOA import PatVoA

def pat_all():
    movie = PatMovie()
    voa = PatVoA()
    speech = PatSpeach()
    id = 0
    id = movie.getArticle(id)
    id = voa.getArticle(id)
    id = speech.getArticle(id)

    print id

pat_all()

# 应用该爬虫时： （1）分别在Speech.py，VOA.py和R_Methode.py 写存库语句；
#              （2）分别改写mp3/lrc/picture的存储路径，分别在Speech.py， VOA.py 和 R_Methode.py 文件中
#              （3）更改六级文件的存储路径，分别在 R_Methode.py 和 K_Methode.py 文件中
#              (4)R_Methode.py 文件中有比较详细的注释
