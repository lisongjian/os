#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: chenjiehua@youmi.net
#

import yaml
import torndb
import datetime
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
    orders = db.query(
        "SELECT * FROM `income` WHERE `day`= %s", today)
    if not orders:
        db.execute("INSERT INTO `income` (`day`) VALUES(%s)", today)

insert()
