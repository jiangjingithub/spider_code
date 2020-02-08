#coding:utf-8
import urllib2
from lxml import etree
from bs4 import BeautifulSoup
class Spider(object):
    def __init__(self):
        self.page = 1
        self.switch = True
    def loadPage(self):
        if self.page == 1:
            url = "http://www.budejie.com/text/"
        else:
            url ="http://www.budejie.com/text/" +str(self.page)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        }
        request = urllib2.Request(url,headers=headers)
        html= urllib2.urlopen(request).read()
        contens = etree.HTML(html)
        list = contens.xpath('//div[@class="j-r-list"]/ul/li/div[@class="j-r-list-c"]/div[@class="j-r-list-c-desc"]/a/@href')
        for temp in list:
            if self.page==1:
                url = url.replace("/text/", "")
            else:
                url = url.replace("/text/"+str(self.page),"")
            fullurl = url + temp
            print fullurl
            self.loadPage1(fullurl,headers)
    def loadPage1(self,fullurl,headers):
        request = urllib2.Request(fullurl, headers=headers)
        html = urllib2.urlopen(request).read()
        contens = etree.HTML(html)
        list = contens.xpath('//div[@class="j-r-list"]/ul/li/div[@class="j-r-list-c"]/div[@class="j-r-list-c-desc"]/h1/text()')
        #soup =BeautifulSoup(html,"lxml")
        #list  = soup.find_all("h1")
        #print list
        self.wirtePage(list)
    def wirtePage(self,list):
        for temp in list:
            temp = temp.encode("utf-8")
            #temp = temp.replace("&ldquo;", "").replace("&rdquo;", "").replace("&hellip;", "").replace("<br />", "")
            with open("D:\duanzi.txt","a") as f:
                f.write(temp+"\n")
    def startWork(self):
        print "抓取百思不得其姐的内涵段子"
        while self.switch:
            self.loadPage()
            key = raw_input("是否继续抓取下一页的段子：（是:y;否:n）")
            if key =="n":
                self.switch = False
            else:
                self.page += 1
if __name__ == "__main__":
    duanzi = Spider()
    duanzi.startWork()
    #duanzi.loadPage()