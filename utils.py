#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2013 Youmi
#
# @author cairuitao@gmail.com, lisongjian@youmi.net
#

""" 辅助类 """

import os.path
import yaml
import hashlib
import logging
root = os.path.curdir


class YamlLoader(yaml.Loader):
    """ Yaml loader

    Add some extra command to yaml.

    !include:
        see http://stackoverflow.com/questions/528281/how-can-i-include-an-yaml-file-inside-another
        include another yaml file into current yaml
    """

    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(YamlLoader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            return yaml.load(f, YamlLoader)


YamlLoader.add_constructor('!include', YamlLoader.include)


def md5_sign(params={}):
    """ 兑吧签名验证 """
    # 排序
    def ksort(d):
        return [(k, d[k]) for k in sorted(d.keys())]

    sorted_params = ksort(params)
    raw_str = ''
    for p in sorted_params:
       raw_str += str(p[1])
    sign = hashlib.new("md5", raw_str).hexdigest()

    return sign

def md5_adxmisign(params={}):
    """ 卡卡签名验证 """
    # 排序
    def ksort(d):
        return [(k, d[k]) for k in sorted(d.keys())]

    sorted_params = ksort(params)
    #print sorted_params
    raw_str = ''
    for p in sorted_params:
       raw_str += str(p[0])+'='+str(p[1])
    raw_str = raw_str+'8b18013079f8a912'
    #print raw_str
    sign = hashlib.new("md5", raw_str).hexdigest()
    #print sign
    return sign

def md5_gofreeadxmisign(params={}, token=''):
    """ 红利签名验证 """
    # 排序
    def ksort(d):
        return [(k, d[k]) for k in sorted(d.keys())]

    sorted_params = ksort(params)
    #print sorted_params
    raw_str = ''
    for p in sorted_params:
       raw_str += str(p[0])+'='+str(p[1])
    raw_str = raw_str+ token
    #print raw_str
    sign = hashlib.new("md5", raw_str).hexdigest()
    #print sign
    return sign


def print_log(log_name, log_path, info):
    """ 日志打印 """
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(message)s')
    fh.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(fh)

    logger.info(info)

def push(self,scopeid,title):
    """推送到Parse"""
    import httplib,json
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/push', json.dumps({
        "where": {
             "scopeid": ""+scopeid+""
        },
        "data": {
             "action": 1,
             "alert": "恭喜，"+title.encode("utf-8")+"兌換成功了。點擊查看"
        }
        }), {
        "X-Parse-Application-Id": self.config['push']['ApplicationId'],
        "X-Parse-REST-API-Key": self.config['push']['APIKey'],
        "Content-Type": "application/json"
         })

def earnPush(self,scopeid, msg, points):
    """推送到Parse"""
    import httplib,json
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/push', json.dumps({
        "where": {
             "scopeid": ""+scopeid+""
        },
        "data": {
             "action": 2,
             "alert": msg.encode("utf-8")+str(points)+u"紅利！"
        }
        }), {
        "X-Parse-Application-Id": self.config['push']['ApplicationId'],
        "X-Parse-REST-API-Key": self.config['push']['APIKey'],
        "Content-Type": "application/json"
         })

def pushover(self,uid,title,msg):
    """Pushover"""
    import urllib,httplib
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
        urllib.urlencode({
            "token": self.config['pushover']['token'],
            "user": self.config['pushover']['user'],
            "message": "uid"+str(uid)+msg,
        }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

def kakapush(self,scopeid,title):
    """推送到Parse"""
    import httplib,json
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/push', json.dumps({
        "where": {
             "scopeid": ""+scopeid+""
        },
        "data": {
             "action": 1,
             "alert": "恭喜，"+title.encode("utf-8")+"兌換成功了。點擊查看"
        }
        }), {
        "X-Parse-Application-Id": self.config['kakapush']['ApplicationId'],
        "X-Parse-REST-API-Key": self.config['kakapush']['APIKey'],
        "Content-Type": "application/json"
         })
