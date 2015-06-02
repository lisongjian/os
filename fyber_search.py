#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: lisongjian@youmi.net
#

import yaml
import torndb
from utils import YamlLoader
import xlrd

SETTINGS_FILE = "settings.yaml"

# MySQL数据库连接配置
try:
    config = yaml.load(file(SETTINGS_FILE, 'r'), YamlLoader)
except yaml.YAMLError as e:
    print "Error in configuration file: %s" % e

# 数据库连接实例
db = torndb.Connection(**config['mysql'])

data = xlrd.open_workbook("Youmi Mobile.xlsx")
for shindex in xrange(0, data.nsheets, 1):
    sh = data.sheet_by_index(shindex)
    for rows in xrange(0, sh.nrows, 1):
        if rows>0:
            row_data = sh.row_values(rows)
            user=db.get("SELECT `user` FROM `callback_order` WHERE `adid` LIKE %s", row_data[0])
            if user:
                print 'user='+str(user['user']) +'&rows='+ str(rows)+'&subid='+row_data[0]
                print user['user']

