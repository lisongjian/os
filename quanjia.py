#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: lisongjian@youmi.net
#

import yaml
import torndb
import urllib,json
from utils import YamlLoader

SETTINGS_FILE = "settings.yaml"
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')
# MySQL数据库连接配置
try:
    config = yaml.load(file(SETTINGS_FILE, 'r'), YamlLoader)
except yaml.YAMLError as e:
    print "Error in configuration file: %s" % e

# 数据库连接实例
db = torndb.Connection(**config['mysql'])

def main():

    for kw in range(961305,1000000):
    #for kw in range(000000,1):
        lenth=len(str(kw))
        if lenth<6:
            kw=str(kw)
            kw=kw.zfill(6)
        url="http://api.map.com.tw/net/familyShop.aspx?searchType=ShopNo&type=&kw=%s&fun=getByName" % kw
        page = urllib.urlopen(url)
        data=page.read()
        data=data.replace('getByName([','').replace('])','')
        print `data`+'======================'
        print `kw` + 'kw'
        d={}
        city=''
        if data=='':
            pass
        elif data!='':
            try:
                d=json.loads(data)
                listcity=['台北市', '新北市', '桃園市', '台中市', '台南巿', '高雄市', \
                          '基隆市', '新竹市', '嘉義市', '新竹縣', '苗栗縣', '彰化縣', \
                          '南投縣', '雲林縣', '嘉義縣', '屏東縣', '宜蘭縣', '花蓮縣', \
                          '台東縣', '澎湖縣', '金門縣', '連江縣']
                cityid=0
                city= d['addr'][0:3]
                try:
                    cityid=listcity.index(city)+1
                    print cityid
                except Exception, ex:
                    print Exception,":",ex
                    pass
                distr= d['addr'][3:6]
                addr= d['addr'][6:]
                db.execute("INSERT INTO `cs_shops` (`type_id`,`name`, `cityid`, `shopstypeid`, `city`, `district`, `street`, `phone`, `lot`, `lat`)  \
                       VALUES(30, %s, %s, 1, %s, %s, %s, %s, %s, %s)", d['NAME'], cityid, city, distr, addr, d['TEL'], d['py'], d['px'])
                time.sleep(0.02)
            except Exception, ex:
                    print Exception,":",ex
                    pass

if __name__=="__main__":
    main()
