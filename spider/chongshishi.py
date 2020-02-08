
from selenium import webdriver
from lxml import etree
import time
import random
import codecs
import pymysql

def gethtml():
    driver = webdriver.PhantomJS()
    url = "http://www.cqcp.net/game/ssc/"
    driver.get(url)
    #print(driver.page_source)
    while True:
        soup = etree.HTML(driver.page_source)
        for each in soup.xpath('//div[@id="openlist"]'):
            issues = each.xpath('..//li[1]/text()')[1:]
            nums = each.xpath('..//li[2]/text()')[1:]
            sum_values = each.xpath('..//li[3]/text()')[1:]
            top_threes = each.xpath('..//li[4]/text()')[1:]
            in_threes = each.xpath('..//li[5]/text()')[1:]
            after_threes = each.xpath('..//li[6]/text()')[1:]
            sum_after_threes = each.xpath('..//li[7]/text()')[1:]
            sum_after_twos = each.xpath('..//li[8]/text()')[1:]
            sizes = each.xpath('..//li[9]/text()')[1:]
        write(issues, nums, sum_values, top_threes, in_threes,
              after_threes, sum_after_threes, sum_after_twos, sizes)
        time .sleep(random.uniform(3, 4))
        driver.find_element_by_id("lnkBtnNext").click()
    driver.quit()

def write(issues, nums, sum_values, top_threes, in_threes,
          after_threes, sum_after_threes, sum_after_twos, sizes):

    for issue, num, sum_value, top_three, in_three, after_three, sum_after_three, sum_after_two, size \
            in zip(issues, nums, sum_values, top_threes, in_threes, after_threes, sum_after_threes, sum_after_twos, sizes):

        #print(issue, num, sum_value, top_three, in_three, after_three, sum_after_three, sum_after_two, size)

        coon = pymysql.connect(host="127.0.0.1", port=3306, db="caipiao", user="root", passwd="890311",
                               charset="gb2312")
        #print('连接mysql成功！！！')
        cursor = coon.cursor()
        sql = "insert into contents(issues, nums, sum_values, top_threes, in_threes, after_threes, sum_after_threes, sum_after_twos, sizes) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, [issue, num, sum_value, top_three, in_three, after_three, sum_after_three, sum_after_two,
                             size])
        coon.commit()
        cursor.close()
        coon.close()
        print("成功写入数据")
        print(issue, num, sum_value, top_three, in_three, after_three, sum_after_three, sum_after_two, size)
        # f = codecs.open("1.txt", "a", encoding="utf-8")
        # f.write(issue+"\t"+num+"\t"+sum_value+"\t"+top_three+in_three+"\t"+after_three+"\t"+sum_after_three+"\t"+sum_after_two+"\t"+size +"\n")
        # f.close()


if __name__ == "__main__":
    gethtml()
