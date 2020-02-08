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
        #开始页
        self.num = 0

    #程序结束后自动调用
    def __del__(self):
        print "抓取数据完成！！！"

    def LoadPage(self,keys):
        #组合连接
        url ="http://cq.58.com/shouji/"+"pn"+str(self.num)+"/?"+keys
        print url
        #首页请求
        request = urllib2.Request(url,headers=self.header)
        html = urllib2.urlopen(request).read()
        #print html
        #用etree解析网页
        soup = etree.HTML(html)
        #提取每款手机连接
        url_list =soup.xpath('//div[@class="infocon"]//td[@class="t"]/a/@href')
        #循环list中的连接
        for newurl in url_list:
            print newurl
            #调用函数LoadPage2并传参数
            self.LoadPage2(newurl)

    def LoadPage2(self,newurl):
        #新网页请求
        request = urllib2.Request(newurl,headers=self.header)
        html = urllib2.urlopen(request).read()
        soup = etree.HTML(html)
        #提取手机详情
        contents = soup.xpath('//div[@class="baby_kuang clearfix"]/p/text()')
        #把contents列表组合成字符串并去掉“|”
        content =",".join(contents).encode("utf-8").replace("|",",")
        #提取价格
        prices = soup.xpath('//div[@class="price_li"]/span/i/text()')
        #print prices
        #提取标题
        titles =soup.xpath('//h1[@class="info_titile"]/text()')
        #print titles
        #调用函数Write并传参数
        self.Write(titles,newurl,content,prices)

    def Write(self,titles,newurl,content,prices):
        #把tiles和prices组合在一个列表中（注：titles和prices列表结构必须相同）
        for title,price in zip(titles,prices):
            #转码utf-8并去掉空格
            title = title.encode("utf-8").replace(" ","")
            price = price.encode("utf-8").replace(" ","")
            #写入文件
            with open("zhuanzhuan.txt","a")as f:
                f.write(newurl+"\t"+title+"\t"+price+"\t"+ content +"\n")
                f.close()

    def StartWork(self):
        keys = raw_input("请输入查询手机型号：")
        #转码为url格式
        keys =urllib.urlencode({"key":keys})
        #print keys
        while True:
            if self.num < 10:
                #每循环一次self.num加1
                self.num +=1
                #暂停5秒抓取数据
                time.sleep(5)
                #调用函数LoadPage并传参数
                self.LoadPage(keys)
            else:
                break


if __name__ =="__main__":
    spider = Spider()
    spider.StartWork()
