#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: chenjiehua@youmi.net
#

import yaml
import torndb
from utils import YamlLoader


SETTINGS_FILE = "settings.yaml"

# MySQL数据库连接配置
try:
    config = yaml.load(file(SETTINGS_FILE, 'r'), YamlLoader)
except yaml.YAMLError as e:
    print "Error in configuration file: %s" % e

# 数据库连接实例
db = torndb.Connection(**config['mysql'])

def reward():
    day = db.get("SELECT DAYOFWEEK(NOW())")['DAYOFWEEK(NOW())']
    # 周日
    if day == 1:
        db.execute("UPDATE `daily_reward` set `status` = 1 \
                   WHERE `ad_id` = 110 or `ad_id` = 104")
        db.execute("UPDATE `daily_reward` set `status` = 0 \
                   WHERE `ad_id` <> 110 and `ad_id` <> 104")
    # 周一周二
    elif day == 2 or day == 3:
        db.execute("UPDATE `daily_reward` set `status` = 1 \
                   WHERE `ad_id` = 109 or `ad_id` = 115")
        db.execute("UPDATE `daily_reward` set `status` = 0 \
                   WHERE `ad_id` <> 109 and `ad_id` <> 115")
    # 周三周四
    elif day == 4 or day == 5:
        db.execute("UPDATE `daily_reward` set `status` = 1 \
                   WHERE `ad_id` = 107 or `ad_id` = 108")
        db.execute("UPDATE `daily_reward` set `status` = 0 \
                   WHERE `ad_id` <> 107 and `ad_id` <> 108")
    # 周五周六
    elif day == 6 or day == 7:
        db.execute("UPDATE `daily_reward` set `status` = 1 \
                   WHERE `ad_id` = 101 or `ad_id` = 103")
        db.execute("UPDATE `daily_reward` set `status` = 0 \
                   WHERE `ad_id` <> 101 and `ad_id` <> 103")

reward()
