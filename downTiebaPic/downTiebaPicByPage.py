# -*- coding: utf-8 -*-
import urllib2
import urllib
import re
import os
import time
import random
import sys

typeEncode = sys.getfilesystemencoding()


class spider:

    def __init__(self):
        self.url = 'http://tieba.baidu.com/p/'
        self.user_agent = [
        'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14)',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5',
        'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
        'Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Maxthon 2.0)',
        'Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10'
        ]
        self.headers = {'User-Agent' : self.user_agent[0]}
        self.lzonly = False

    def loadTiezi(self):
        ID = raw_input('请输入帖子的编号：\n')
        lzonly = input('是否开启只看楼主？(1、是 2、否)\n')
        self.url = 'http://tieba.baidu.com/p/' + ID
        if(lzonly == 1):
            self.lzonly = True
        if self.lzonly:
            self.url += '?see_lz=1'
        self.request = urllib2.Request(self.url,headers = self.headers)
        self.response = urllib2.urlopen(self.request)
        self.content = self.response.read().decode('utf-8')
        self.response.close()
        print u'帖子载入成功'
        tppat = re.compile('"total_page":(\d+)};')
        tp = re.findall(tppat,self.content)
        self.total_page = int(tp[0])
        titlepat = re.compile('<title>(.*?)</title>')
        tl = re.findall(titlepat,self.content)
        self.title = tl[0]
        self.showPageInfo()


    def showPageInfo(self):
        print u'帖子标题：%s' %self.title
        print u'总页数：%d' %self.total_page


    def makeDir(self,path):
        exist = os.path.exists(path)
        if not exist:
            os.makedirs(path)
            return True
        else:
            return False

    def changePage(self,newpage):
        if self.lzonly:
            url = self.url + '&pn=' + str(newpage)
        else:
            url = self.url + '?pn=' + str(newpage)
        #print url
        self.headers = {'User-Agent' : self.user_agent[newpage % 10]}
        request = urllib2.Request(url,headers = self.headers)
        response = urllib2.urlopen(request,timeout = 60)
        content = response.read().decode('utf-8')
        response.close()
        return content

    def downPics(self):
        path = self.title
        self.makeDir(path)
        picpat = re.compile('<img class="BDE_Image" .*?src="(.*?)".*?<br>',re.S)
        page = input("请输入你要抓取的页码(0退出)\n")
        while(page > 0 & page <= self.total_page):
            self.content = self.changePage(page)
            num = 1
            pics = re.findall(picpat,self.content)
            for pic in pics:
                f = open(path + "/page_" + str(page) + "_" + str(num) + '.jpg',"wb")
                u = urllib.urlopen(pic)
                data = u.read()
                f.write(data)
                print u'page_' + str(page) + u'_' + str(num) + u'.jpg保存成功'
                f.close()
                num += 1
                time.sleep(random.uniform(1,2))
            page = input("请输入你要抓取的页码(0退出)\n")






    def start(self):
        run = True
        print u'欢迎使用百度贴吧图片下载器'
        self.loadTiezi()
        while (run):
            option = input("1、载入帖子\n2、查看帖子详情\n3、下载图片\n4、退出\n")
            if(option==1):
                self.loadTiezi()
            elif(option==2):
                self.showPageInfo()
            elif(option==3):
                self.downPics()
            elif(option==4):
                run = False






tieba = spider()
tieba.start()
