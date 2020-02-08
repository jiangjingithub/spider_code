#coding:utf-8
import urllib2
from lxml import etree
import re
import os

class Spider(object):
    def __init__(self):
        self.header ={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36"

        }
        self.url="https://www.geyanw.com/"
    def __del__(self):
        #程序结束自动调用
        print "数据写入完成！！！"

    def loadPage(self):
        request =urllib2.Request(self.url,headers=self.header)
        html=urllib2.urlopen(request).read()
        #print html
        # 按xpath解析网页
        contents=etree.HTML(html)
        #取出格言内容链接
        lists =contents.xpath('//ul[@class="d1 ico3"]/li/a/@href')
       # print lists
        for new_url in lists:
            #print new_url
            #组合成每个格言网址
            fullurl=self.url+new_url
            print fullurl
            self.newPage(fullurl)

    def newPage(self,fullurl):
        request=urllib2.Request(fullurl,headers=self.header)
        html=urllib2.urlopen(request).read()
        #print html
        #按xpath解析网页
        content=etree.HTML(html)
        #取标题
        title_list=content.xpath('//div[@id="container"]//div[@class="title"]/h2/text()')
        #print title_list
        #取内容
        gy_list=content.xpath('//*[@id="p_left"]/div[1]/div[4]/p/text()')
        #print type(title_list)
        #合并两个列表
        title_list.extend(gy_list)
        #print title_list
        self.write(title_list)
    def write(self,title_list):
        #os.remove("geyan.txt")
        #循环列表
        for title in title_list:
            print title
            #转码
            title=title.encode("utf-8")
            #打开文件写入文件
            with open("geyan.txt","a")as f:
                f.write(title+"\n")

if __name__ =="__main__":
    spider=Spider()
    spider.loadPage()