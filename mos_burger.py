#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author cairuitao@gmail.com
#

""" 抓取优惠券信息 """

import urllib2
import yaml
import torndb
import time

from bs4 import BeautifulSoup
from utils import YamlLoader

# load mysql config
config = yaml.load(file('settings.yaml', 'r'), YamlLoader)
db = torndb.Connection(**config['mysql'])


dict1=[('臺北市',1),('新北市',2), ('桃園縣',3),('臺中市',4),('臺南市',5),('高雄市',6), \
       ('基隆市',7),('新竹市',8), ('嘉義市',9), ('新竹縣',10),('苗栗縣',11), ('彰化縣',12),  \
       ('南投縣',13), ('雲林縣',14), ('嘉義縣', 15), ('屏東縣', 16), ('宜蘭縣',17), \
       ('澎湖縣',20), ('金門縣',21)]


url = 'http://www.mos.com.tw/shopSearch.php?servicelist=all&zip01sel='
url_test = 'http://www.mos.com.tw/shopSearch.php?servicelist=all&zip01sel=%E8%8A%B1%E8%93%AE%E7%B8%A3'

# 伪造UA
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'}

def crawl_html(url):
    """ 将指定url抓取转化为soup """

    print(url)
    req = urllib2.Request(url, None, headers)
    return BeautifulSoup(urllib2.urlopen(req).read())

def insert_db(cityid, city, url_in):
    soup=crawl_html(url_in)
    get = soup.find("div", class_="shopList")
    shops=get.find_all("dl")
    for s in shops:
        #print s
        name = s.find('a').get_text()
        add_tel = s.find_all('dd')
        addr=add_tel[0].get_text()
        distr=addr[3:6]
        street=addr[6:]
        tel=add_tel[1].get_text()
        db.execute("INSERT INTO `cs_shops` (`type_id`,`name`, `cityid`, `shopstypeid`, `city`, `district`, `street`, `phone`, `lot`, `lat`)  \
                   VALUES(50, %s, %s, 3, %s, %s, %s, %s, %s, %s)", name, cityid, city, distr, street, tel, 0, 0)
        time.sleep(0.5)

for d in dict1:
    city_name=d[0]
    city_id=d[1]
    url_in=url+d[0]
    insert_db(city_id,city_name, url_in)


if __name__ == "__main__":
    print 'ok'
