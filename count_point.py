#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: lisongjian@youmi.net
#

import yaml
import torndb
import datetime
from datetime import timedelta
from utils import YamlLoader


SETTINGS_FILE = "settings.yaml"

# MySQL数据库连接配置
try:
    config = yaml.load(file(SETTINGS_FILE, 'r'), YamlLoader)
except yaml.YAMLError as e:
    print "Error in configuration file: %s" % e

# 数据库连接实例
db = torndb.Connection(**config['mysql'])

def insert():
    today = datetime.datetime.today().date()
    yesterday = today-timedelta(days=1)
    orders = db.query(
        "SELECT * FROM `count_point` WHERE `day`= %s", today)
    if not orders:
        total_earn = db.query("SELECT a.uid, b.user,b.time, b.ad_source, sum(b.points) FROM `user` AS a, `callback_order` AS b WHERE a.uid = b.user AND b.ad_source>=100 AND a.`create_at` BETWEEN %s \
        AND %s AND b.`time` BETWEEN %s AND %s GROUP BY b.points WITH ROLLUP ", yesterday, today, yesterday, today).pop()['sum(b.points)']
        aos_earn = db.query("SELECT a.uid,a.platform, b.user, sum(b.points), b.time, b.ad_source FROM `user` AS a, `callback_order` AS b WHERE a.uid = b.user AND a.`create_at` BETWEEN %s \
        AND %s AND b.`time` BETWEEN %s AND %s AND b.ad_source>=100 AND a.platform=1 GROUP BY b.points WITH ROLLUP ", yesterday, today, yesterday, today).pop()['sum(b.points)']
        ios_earn = db.query("SELECT a.uid,a.platform, b.user, sum(b.points), b.time, b.ad_source FROM `user` AS a, `callback_order` AS b WHERE a.uid = b.user AND a.`create_at` BETWEEN %s \
        AND %s AND b.`time` BETWEEN %s AND %s AND b.ad_source>=100 AND a.platform=2 GROUP BY b.points WITH ROLLUP ", yesterday, today, yesterday, today).pop()['sum(b.points)']
        free = db.query("SELECT a.uid,a.appType, b.user, sum(b.points), b.time, b.ad_source FROM `user` AS a, `callback_order` AS b WHERE a.uid = b.user AND a.`create_at` BETWEEN %s \
        AND %s AND b.`time` BETWEEN %s AND %s AND b.ad_source>=100 AND a.appType=0 GROUP BY b.points WITH ROLLUP ", yesterday, today, yesterday, today).pop()['sum(b.points)']
        kaka = db.query("SELECT a.uid,a.appType, b.user, sum(b.points), b.time, b.ad_source FROM `user` AS a, `callback_order` AS b WHERE a.uid = b.user AND a.`create_at` BETWEEN %s \
        AND %s AND b.`time` BETWEEN %s AND %s AND b.ad_source>=100 AND a.appType=1 GROUP BY b.points WITH ROLLUP ", yesterday, today, yesterday, today).pop()['sum(b.points)']
        ch = db.query("SELECT a.uid,a.en, b.user, sum(b.points), b.time, b.ad_source FROM `user` AS a, `callback_order` AS b WHERE a.uid = b.user AND a.`create_at` BETWEEN %s \
        AND %s AND b.`time` BETWEEN %s AND %s AND b.ad_source>=100 AND a.en=0 GROUP BY b.points WITH ROLLUP ", yesterday, today, yesterday, today).pop()['sum(b.points)']
        en = db.query("SELECT a.uid,a.en, b.user, sum(b.points), b.time, b.ad_source FROM `user` AS a, `callback_order` AS b WHERE a.uid = b.user AND a.`create_at` BETWEEN %s \
        AND %s AND b.`time` BETWEEN %s AND %s AND b.ad_source>=100 AND a.en=1 GROUP BY b.points WITH ROLLUP ", yesterday, today, yesterday, today).pop()['sum(b.points)']
        db.execute("INSERT INTO `count_point` (`day`,`total_earn`, `aos`, `ios`, `kaka`, `gofree`, `en_earn`, `ch_earn`)  \
                   VALUES(%s,%s, %s, %s, %s, %s, %s, %s)", yesterday, total_earn, aos_earn, ios_earn, kaka, free, en, ch)

insert()
