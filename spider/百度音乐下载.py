import requests
import re
import urllib.parse
import string
import os
import time
import random
from threading import Thread
from queue import Queue

class Baidu(object):
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
                        }
        self.pagequeue = Queue()
    def page(self, name):
        """访问歌曲的首页，取出歌曲id"""
        data = {"key": name}
        #转码
        data = urllib.parse.urlencode(data)
        num = 0
        while True:
            #组合链接
            url = "http://music.baidu.com/search/song?s=1&"+str(data)+"&jump=0&start="+str(num)+"&size=20&third_type=0"
            #发送首页请求
            res = requests.get(url, headers=self.headers, params=data)
            #print(res.url)
            #解析网页
            html = res.text
            #print(html)
            #取歌的ID
            song_id = re.findall(r'sid&quot;:(\d+)', html)
            #取共搜索到多少歌+
            song_num = re.findall(r'<span class="number">(\d+)</span>', html)[0]
            print("共搜索到%s" % song_num)
            #转成数字类型
            song_num = int(song_num)
            #print(num)
            #print(song_id)
            #调用函数
            self.page2(song_id)
            #num小余song_num，num加20否则就退出循环
            if num < song_num:
                num += 20
            else:
                break

    def single_page(self, name):
        """访问歌曲的首页，取出歌曲id"""
        ids = []
        data = {"key": name}
        url = "http://music.baidu.com/search?"
        # 发送首页请求
        res = requests.get(url, headers=self.headers, params=data)
        print(res.url)
        # 解析网页
        html = res.text
        # print(html)
        # 取歌的ID
        song_id = re.findall(r'sid&quot;:(\d+)', html)[0]
        ids.append(song_id)
        #print(ids)
        self.page2(ids)

    def page2(self, song_id):
        """取出下载歌曲的链接和歌的标题"""
        for each in song_id:
            #组合链接
            url = "http://tingapi.ting.baidu.com/v1/restserver/ting?method=baidu.ting.song.play&format=jsonp&callback="\
                  "jQuery172033069761867241043_1513693323115&songid=%s&_=1513693324851" % each
            #发送网页请求
            res = requests.get(url, headers=self.headers)
            html = res.text
            #print(html)
            #用正则取出歌曲下载链接
            download_link = re.findall(r'"file_link":"(.+)",', html)[0].replace("\\", "")
            #print(download_link)
            #用正则取出每首歌曲标题
            title = re.findall(r'"title":"(.+)",', html)[0].split(",")[0]
            #text为所有标点
            text = string.punctuation
            #替换歌曲名中的所有标点，防止系统不能建立文件夹
            for temp in text:
                if temp in title:
                    title = title.replace(temp, "")
            #调用下载函数
            time.sleep(random.uniform(2, 4))
            self.download(download_link, title)
            #print(title)
            #print(download_link)

    def download(self, download_id, title):
        """下载歌曲"""
        content = requests.get(download_id, headers=self.headers).content
        #判断MP3文件是否存在，不存在就写入
        if title not in os.path.basename("./"):
            #写入文件
            with open(title+".mp3", "wb")as f:
                print("正在下载%s..." % title)
                f.write(content)
                f.close()
                print("%s下载完成！！！" % title)

    def single_start(self):
        """下载单曲的调度"""
        name = input("输入你要下载的歌曲:")
        print("下载%s单曲" % name)
        self.single_page(name)
        while True:
            key = input("是否继续下载歌曲！！(是：Y；否：N；退出单曲下载：任意键)")
            key = key.lower()
            if key == "y":
                name = input("输入你要下载的歌曲：")
                self.single_page(name)
            elif key == "n":
                break
            else:
                self.start()

    def whole_start(self):
        """下载歌手全部歌曲的调度"""
        name = input("输入你要下载的歌曲的歌手:")
        print("下载%s全部歌曲" % name)
        self.page(name)

        while True:
            key = input("是否继续下载歌曲！！(是：Y；否：N；退出下载歌手全部歌曲：任意键)：")
            key = key.lower()
            if key == "y":
                name = input("输入你要下载的歌曲：")
                self.page(name)
            elif key == "n":
                break
            else:
                self.start()

    def start(self):
        """控制程序"""
        text = input("1.下载单曲(歌名+歌手)；2.下载歌手全部歌曲：")
        if text == "2":
            self.whole_start()
        elif text == "1":
            self.single_start()
        else:
            print("输入有误！！！")
            #输入有误重新调用start
            self.start()

if __name__ == "__main__":
    spider = Baidu()
    spider.start()
