#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2015
#
# @author: lisongjian@youmi.net
#

"""自动兑换
使用crontab定时任务，每天01:15统计前天数据，部分数据如：
兑换订单由于审核状态修改，需重复统计前3天以获得准确数据。
"""

from __future__ import division
import yaml
import torndb
import db
from utils import YamlLoader

SETTINGS_FILE = "settings.yaml"

# MySQL数据库连接配置
try:
        config = yaml.load(file(SETTINGS_FILE, 'r'), YamlLoader)
except yaml.YAMLError as e:
        print "Error in configuration file: %s" % e

# 数据库连接实例
db.mysql = torndb.Connection(**config['mysql'])

def auto_change():
    all_orders=db.mysql.query(
        "SELECT * FROM `exchange_orders` WHERE `goods_id` NOT IN (86,87,88) AND `status`=0 AND `duiba`=0")
    print all_orders
    for order in all_orders:
        userinfo=db.mysql.get(
            "SELECT * FROM `user` WHERE `uid`=%s", order['uid'])
        print userinfo

def main():
    auto_change()
if __name__ == "__main__":
    main()
