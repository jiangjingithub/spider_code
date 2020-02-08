import requests
from lxml import etree
import csv
import os
import time
import pandas
class Spider(object):
    def __del__(self):
        print("抓取完成！！！")

    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
                        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
                        }
        self.num = 1
        self.url = "http://esf.cq.fang.com"

    def LoadPage(self):
        if self.num == 1:
            url = "http://esf.cq.fang.com/"
        else:
            url = "http://esf.cq.fang.com/house/i3"+str(self.num)+"/"
        print(url)
        #requests模块发送get请求
        response = requests.get(url, headers=self.headers)
        #取出response数据
        html = response.text
        #按etree.HTML解析html
        soup = etree.HTML(html)
        #取出每个在出售的房子连接
        links =soup.xpath('//dd[@class="info rel floatr"]/p[@class="title"]/a/@href')
        #print links
        #循环links列表取出连接
        for link in links:
            new_url = self.url+link
            #print(new_url)
            self.LoadPage2(new_url)

    def LoadPage2(self, new_url):
        #创建一个空列表用于存储取出的信息
        all_list = []
        # requests模块发送get请求
        response = requests.get(new_url, headers=self.headers)
        #取出response数据
        html = response.text
        #print(html)
        soup = etree.HTML(html)
        #取标题
        titles = soup.xpath('//div[@class="wid1200 clearfix"]/div[1]/div[1]/text()')
        #把titles列表连接成字符串并取出不需要的数据
        title = "".join(titles).replace("\r", "").replace("\n", "").replace(" ", "").replace("?", "")
        list1 = soup.xpath('//div[@class="content-item"]//div[@style="font-size:14px;"]//text()|//div[@class="content-item"]//div[@style="FONT-SIZE: 14px"]//text()')
        content = "".join(list1).replace("\r", "").replace("\n", "").replace("\xa0", "").replace(" ", "").replace("\u2003", "").replace('\u2022', '')
        link_list = soup.xpath('//div[@class="cont-sty1 clearfix"]//div[@class="item ls_cl"]/img/@data-src|//div[@class="cont-sty1 clearfix"]//div[@class="item "]/img/@data-src')
        self.LoadImg(link_list, title)
        #print(link_list)

        for each in soup.xpath('//div[@class="tab-cont-right"]'):
            # 取价格
            prices = each.xpath('./div[2]/div[1]/i/text()')
            price ="".join(prices)
            #取户型
            houses = each.xpath('./div[3]/div[1]/div[1]/text()')
            house ="".join(houses).replace("\r", "").replace("\n", "")
            #取面积
            acreages = each.xpath('./div[3]/div[2]/div[1]/text()')
            acreage = "".join(acreages).replace("平米", "㎡")
            #取单价
            unit_prices = each.xpath('./div[3]/div[3]/div[1]/text()')
            unit_price = "".join(unit_prices).replace("平米", "㎡")
            #取朝向
            directions = each.xpath('./div[4]/div[1]/div[1]/text()')
            direction ="".join(directions)
            #取楼层
            floors = each.xpath('./div[4]/div[2]/div[1]/text()')
            floor = "".join(floors)
            #总楼层
            total_floors = each.xpath('./div[4]/div[2]/div[2]/text()')
            total_floor = "".join(total_floors)
            #取装修
            decorations = each.xpath('./div[4]/div[3]/div[1]/text()')
            decoration = "".join(decorations)
            #小区
            villages = each.xpath('./div[5]/div[1]/div[2]/a[@class="blue"]/text()')
            village = "".join(villages)
            #区域
            areas = each.xpath('./div[5]/div[2]/div[2]/a/text()')
            area = "".join(areas).replace("\r","").replace("\n", "").replace(" ", "")
        for temp in soup.xpath('//div[@class="wid1200 clearfix"]/div[2]'):
            #取建筑年代
            years = temp.xpath('./div[2]/div[1]/span[2]/text()')
            year = "".join(years)
            #取有无电梯
            lifts = temp.xpath('./div[2]/div[2]/span[2]/text()')
            lift ="".join(lifts)
            #产权性质
            styles = temp.xpath('./div[2]/div[3]/span[2]/text()')
            style = "".join(styles)
        #往all_list增加取出的数据
        all_list.append([new_url, title, price, house, acreage, unit_price ,
                          direction, floor, decoration, total_floor, village, area, year, lift, style, content])
        #print(all_list)
        self.Write(all_list)

    def Write(self, all_list):
        with open("fangtianxia.csv", "a") as f:
            #初始化csv写入
            writer = csv.writer(f)
            #按行写入一下内容
            writer.writerow(["网址", "标题", "价格","户型", "面积", "单价", "朝向",
                             "楼层", "装修", "总楼层", "小区", "区域", "建筑年代", "有无电梯", "产权性质", "房屋详情"])
            for temp in all_list:
               # 按行写入all_list数据
                writer.writerow(temp)

    def LoadImg(self, link_list, title):
        if(not os.path.exists(title)):
            #创建一个文件用于存图片
            os.mkdir(title)
            #跳到建立的文件内
            os.chdir(title)
        else:
            os.chdir(title)
        for link in link_list:
            print(link)
            if "http" in link:
                response = requests.get(link, headers=self.headers)
                img = response.content
                #取图片名字
                filename = link[-20:].replace("/", "")
                #写入图片
                with open(filename, "wb") as f:
                    f.write(img)
                    f.close()
            #跳出刚才建立的文件到py文件夹中
        os.chdir("../")

    def StartWork(self):
        while True:
            if self.num < 100:
                time.sleep(5)
                self.LoadPage()
                self.num += 1
            else:
                break

if __name__ =="__main__":
    spider = Spider()
    spider.StartWork()