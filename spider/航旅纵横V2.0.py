#coding:utf-8
import urllib2
import urllib
import json
import jsonpath
import datetime
import os
import glob
class hangLv():
    def __init__(self):
        self.headers ={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36"}
    def __del__(self):
        print "******数据抓取完成！！！******"

    def urlHandle(self,dep,arr,date):
        #处理请求网页数据
        data = {
            "dep": dep,
            "arr":arr,
            "begDate": date
        }
        #转码
        data = urllib.urlencode(data)
        url="http://www.umetrip.com/mskyweb/tk/dm.do?"
        self.loadPage(url,data)

    def loadPage(self,url,data):
        #网页请求
        request= urllib2.Request(url,data=data,headers=self.headers)
        html=urllib2.urlopen(request).read()
        self.writePage(html)

    def writePage(self,html):
        #解析json
        alllist = json.loads(html)
        #取出json数据
        hblists = jsonpath.jsonpath(alllist,"$..pflydate,pflynum,pbegcode,pendcode,pbegtime,pendtime,code,price,seatNum")
        #循环去除多于数据并写入文件
        for hblist in hblists:
            #创造换行
            hblist = hblist.replace("2017","\n2017").replace("----"," ")
            #去掉无用信息
            hblist= hblist.encode("utf-8").replace("票量充足","9").replace("剩余","").replace("张","")
            #写入数据到文件
            with open("hangban.txt","a")as f :
                print hblist
                f.write(hblist+"\t")
                f.close()

    def startWork(self):
        try:
            #删除文件
            os.remove("hangban.txt")
        except:
            pass
        #读取当前文件夹的所有txt文件，返回的是list
        filename = glob.glob("*.txt")
        if len(filename):
            for each in filename:
                with open(each,"r")as f:
                    # 每行依次读取文件
                    str_list= f.readlines()
                #起始行号
                    num=0
                    for temp in str_list:
                        #行号依次加1
                        num +=1
                        #检查程序异常
                        try:
                            #按，号取文件内容
                            dep = str(temp.split(",")[0])
                            arr = str(temp.split(",")[1])
                            start_time = str(temp.strip().split(',')[2])
                            end_time=str(temp.strip().split(",")[3])
                            #把时间字符串转换为时间
                            start_time=datetime.datetime.strptime(start_time,"%Y-%m-%d")
                            end_time =datetime.datetime.strptime(end_time,"%Y-%m-%d")
                            #建立一个空列表
                            list_days=[]
                            #循环取出时间
                            for i in range((end_time-start_time).days+1):
                                day = start_time + datetime.timedelta(days=i)
                                day=str(day)[:10]
                                #把day增加到list_days里
                                list_days.append(day)
                                #循环list-days列表，并调用urlHandle
                            for date in list_days:
                                print dep+ "-" + arr + date
                                self.urlHandle(dep,arr,date)
                        #程序异常执行下面代码
                        except:
                            #检查程序异常
                            try:
                                dep=str(temp.split(",")[0])
                                arr=str(temp.split(",")[1])
                                start_time=str(temp.strip().split(',')[2])
                                self.urlHandle(dep, arr, start_time)
                            #程序异常执行下面程序
                            except:
                                print "查询的数据有误！！！"
                f.close()
        else:
            print "没有查询数据文件,请增加查询数据文件！！！"
if __name__ =="__main__":
    spider = hangLv()
    spider.startWork()
