#!/usr/bin/env python
# encoding:utf-8
import re
import urllib
import urllib2
import urlparse
import json
import os
from bs4 import BeautifulSoup
class spider(object):
    def __init__(self):
        self.four = None
        self.fileDir = None
    #文件下载
    def retrieve(self,url,filename):
        filepath = self.fileDir+os.sep+filename.strip()+'.mp4'
        fileName,httpMessage = urllib.urlretrieve(url,filepath,reporthook=None)
        # print '文件名 %s  下载进度:HttpMessage %s' % (fileName.encode('utf-8') , httpMessage)

    def parse_DownUrl(self,url,filename):
        # id = re.compile(ur"\d+").search('u'+url).group() 正则取到最后的id
        id = url.split('/')[-1]
        realUrl = self.getRealUrl(id)
        self.four.write('\n'+realUrl.encode('utf-8'))
        self.retrieve(realUrl,filename)#下载视频
        print realUrl
    def creatdir(self,fileInfo):
        self.fileDir = fileInfo
        if os.path.exists(self.fileDir) == False:
            os.mkdir(self.fileDir)

    def craw(self,vid,quality='H'):
        suffix = vid
        if isinstance(vid,int):
            suffix = '%d'%vid
        url = 'http://www.imooc.com/learn/' + suffix
        html_cont = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
        title = soup.h2.get_text()
        self.creatdir(fileInfo=title)
        filepath = self.fileDir+os.sep+title.strip()+'.txt'
        self.four = open(filepath,'w')
        chapter_nodes = soup.find_all('div',class_='chapter')
        # print chapter_nodes
        for chapter in chapter_nodes:
           chapterName = chapter.find('strong').get_text()
           print chapterName
           self.four.write('\n' + chapterName.encode('utf-8'))
           sub_nodes = chapter.find_all('a',href=re.compile(r"/video/\d+"))
           for node in sub_nodes:
                subchapterName = re.sub(r'\(.*\)','',node.get_text())
                self.four.write('\n'+subchapterName.encode('utf-8'))
                print subchapterName
                old_url = urlparse.urljoin(url,node['href'])
                self.parse_DownUrl(old_url,subchapterName)
    def getRealUrl(self,id):
        url = 'http://www.imooc.com/course/ajaxmediainfo/?mid=%s&mode=flash' % id
        req = urllib2.urlopen(url)
        data = json.load(req)
        return data['data']['result']['mpath'][2]
imooc_spider = spider()
vid = raw_input('请输入需要抓取的慕课网视频id:')
imooc_spider.craw(vid)
