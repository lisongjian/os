#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: lisongjian@youmi.net
#

import yaml
import torndb
import urllib2,json
from utils import YamlLoader

SETTINGS_FILE = "settings.yaml"
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
    url='http://www.google.com'
    page = urllib2.urlopen(url).geturl()
    #addr='雲林縣西螺鎮振興里2號(北上)'
    #url="http://www.google.com/maps/search/%s/" % addr
    #page = urllib2.urlopen(url).geturl()
    print `page`

if __name__=="__main__":
    main()
