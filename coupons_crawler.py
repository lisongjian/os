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
import os.path
import torndb

from datetime import datetime
from bs4 import BeautifulSoup
from utils import YamlLoader
from urlparse import urlparse

# 优惠券抓取页面
base_url = "http://m.5ikfc.com"
coupons_list_urls = (
    (("肯德基", 1), "http://m.5ikfc.com/kfcm/"),
    (("麦当劳", 2), "http://m.5ikfc.com/mdl/"),
    (("真功夫", 3), "http://m.5ikfc.com/zkf/")
)

# 伪造UA
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'}

# static 文件存放地址
static_path = os.path.join(os.path.dirname(__file__), "static")

# load mysql config
config = yaml.load(file('settings.yaml', 'r'), YamlLoader)
db = torndb.Connection(**config['mysql'])


def crawl_html(url):
    """ 将指定url抓取转化为soup """

    print(url)
    req = urllib2.Request(url, None, headers)
    return BeautifulSoup(urllib2.urlopen(req).read())


def crawl_coupons(coupons_url):
    """ 根据tuple抓取优惠券 """

    typ, url = coupons_url
    soup = crawl_html(url)
    coupons_links = soup.find("div", class_="brand_wrap").find_all('a')

    for link in coupons_links:
        href = base_url + link['href']
        crawl_single_coupon(typ, href)


def crawl_single_coupon(typ, href):
    """ 抓取单个优惠券 """

    soup = crawl_html(href)
    coupon_id = href.split("/")[-2]

    exists = db.get("SELECT coupon_id FROM coupons WHERE coupon_id = %s", coupon_id)
    if exists:
        return

    # 抓取原始信息
    meta = soup.find("div", class_="brand_wrap")
    title = meta.h3.string.encode('utf-8')
    if "：" in title:
        title = title.split("：")[1]
    valid_time = meta.find("span", class_="valid").string
    if not valid_time:
        return

    coupons_img = soup.find("img", class_="couponimg")
    if coupons_img:
        img_url = coupons_img["src"]
    else:
        return

    img_name = os.path.basename(urlparse(img_url).path)

    # 下载优惠券图片
    now = datetime.now()
    img_path = os.path.join(os.path.join(os.path.join("coupons", str(now.year)), str(now.month)), img_name)
    img_store_path = os.path.join(static_path, img_path)

    base_dir = os.path.dirname(img_store_path)
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    if not os.path.exists(img_store_path):
        with open(img_store_path, 'wb+') as output:
            output.write(urllib2.urlopen(img_url).read())

    # 解析出有效期
    end_date_zh = valid_time[4:].encode("utf-8")
    end_date = datetime.strptime(end_date_zh, "%Y年%m月%d日")

    db.execute(
        "INSERT INTO `coupons` (coupon_id, brand_id, title, img,"
        "end_date) VALUES (%s, %s, %s, %s, %s)",
        coupon_id, typ[1], title, img_path, end_date)


if __name__ == "__main__":
    count = 0
    for coupons_url in coupons_list_urls:
        count +=1
        print 'save ' + `count`
        crawl_coupons(coupons_url)
