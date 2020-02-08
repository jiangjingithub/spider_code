#coding:cp936
import urllib2
import urllib
from lxml import etree
import time
class Spider():
    def __init__(self):
        self.header ={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
                      "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"

        }
        #��ʼҳ
        self.num = 0

    #����������Զ�����
    def __del__(self):
        print "ץȡ������ɣ�����"

    def LoadPage(self,keys):
        #�������
        url ="http://cq.58.com/shouji/"+"pn"+str(self.num)+"/?"+keys
        print url
        #��ҳ����
        request = urllib2.Request(url,headers=self.header)
        html = urllib2.urlopen(request).read()
        #print html
        #��etree������ҳ
        soup = etree.HTML(html)
        #��ȡÿ���ֻ�����
        url_list =soup.xpath('//div[@class="infocon"]//td[@class="t"]/a/@href')
        #ѭ��list�е�����
        for newurl in url_list:
            print newurl
            #���ú���LoadPage2��������
            self.LoadPage2(newurl)

    def LoadPage2(self,newurl):
        #����ҳ����
        request = urllib2.Request(newurl,headers=self.header)
        html = urllib2.urlopen(request).read()
        soup = etree.HTML(html)
        #��ȡ�ֻ�����
        contents = soup.xpath('//div[@class="baby_kuang clearfix"]/p/text()')
        #��contents�б���ϳ��ַ�����ȥ����|��
        content =",".join(contents).encode("utf-8").replace("|",",")
        #��ȡ�۸�
        prices = soup.xpath('//div[@class="price_li"]/span/i/text()')
        #print prices
        #��ȡ����
        titles =soup.xpath('//h1[@class="info_titile"]/text()')
        #print titles
        #���ú���Write��������
        self.Write(titles,newurl,content,prices)

    def Write(self,titles,newurl,content,prices):
        #��tiles��prices�����һ���б��У�ע��titles��prices�б�ṹ������ͬ��
        for title,price in zip(titles,prices):
            #ת��utf-8��ȥ���ո�
            title = title.encode("utf-8").replace(" ","")
            price = price.encode("utf-8").replace(" ","")
            #д���ļ�
            with open("zhuanzhuan.txt","a")as f:
                f.write(newurl+"\t"+title+"\t"+price+"\t"+ content +"\n")
                f.close()

    def StartWork(self):
        keys = raw_input("�������ѯ�ֻ��ͺţ�")
        #ת��Ϊurl��ʽ
        keys =urllib.urlencode({"key":keys})
        #print keys
        while True:
            if self.num < 10:
                #ÿѭ��һ��self.num��1
                self.num +=1
                #��ͣ5��ץȡ����
                time.sleep(5)
                #���ú���LoadPage��������
                self.LoadPage(keys)
            else:
                break


if __name__ =="__main__":
    spider = Spider()
    spider.StartWork()
