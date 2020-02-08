import requests
import pymysql

class Spider(object):

    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                      "Chrome/63.0.3239.132 Safari/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/"
                                  "apng,*/*;q=0.8",
                        "Host": "www.cwl.gov.cn",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9",
                        "Cache-Control": "max-age=0",
                        "Connection": "keep-alive",
                        "Referer": "http://www.cwl.gov.cn/",
                        "Upgrade-Insecure-Requests": "1"
                        }

    def __del__(self):
        print("抓取数据完成！！！")

    def load_page(self):
        s = requests.session()
        s.headers.update(self.headers)
        url = "http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?"
        params = {"name": "ssq", "issueCount": "100"}
        r = s.get("http://www.cwl.gov.cn/")
        #print(r.text)
        req = s.get(url, params=params,)
        #print(req.url)
        html = req.json()
        #print(html)
        for each in html["result"]:
            code = each["code"]
            date = each["date"]
            red = each["red"]
            blue = each["blue"]
            self.write_mysql(code, date, red, blue)
    def write_mysql(self,code, date, red, blue):
        coon = pymysql.connect(host="127.0.0.1", port=3306, db="fulicaipiao", user="root", passwd="890311",
                               charset="utf8")
        #print("链接成功！！！")
        cursor = coon.cursor()
        sql = "insert into contents (code,date,red,blue)values(%s,%s,%s,%s)"
        try:
            print("正在写入数据库！！！")
            cursor.execute(sql, [code, date, red, blue])
            coon.commit()
            cursor.close()
            coon.close()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    spider = Spider()
    spider.load_page()