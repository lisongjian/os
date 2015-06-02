#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

广告平台回调处理
@author lisongjian@youmi.net

"""

from urllib import unquote
from protocols import JSONBaseHandler
import logging
import logging.config
import json,httplib
import utils
import hashlib


class CallbackHandler(JSONBaseHandler):
    logger = None  # logger handler

    def get(self, platform):
        """接收广告平台回调"""
        if platform == 'personaly' :
            platform = 'aos'
            self.__save_persona_order(platform)
            self.write('ok')
            self.__log(self.ip)
        if platform == 'personalyios' :
            platform = 'ios'
            self.__save_persona_order(platform)
            self.write('ok')
            self.__log(self.ip)

    def __save_persona_order(self, platform):
        params = {}
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1", self.ip)
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            return
        self.params={}
        params['sign'] = self.get_argument('sign', '')
        params['scopeid'] = unquote(self.get_argument('user_id', ''))
        params['getPoint'] = self.get_argument('amount', '')
        params['order'] = self.get_argument('offer_id', '')
        params['app'] = self.get_argument('app_id', '')
        params['sig'] = self.get_argument('signature', '')
        params['offer_name'] = unquote(self.get_argument('offer_name', ''))
        detail = platform + " ( 应用名:"+ params['offer_name'] + ") personaly红利"
        params['ad'] = "personaly紅利"
        if platform=='aos':
            appHash='053d607e3f208231e628eb923bf0d451'
            key='449720b64a77d28087b2767233a4ab2f'
            pF=3
        elif platform=='ios':
            appHash='c1ec530fc34a7f6194195614079ca51e'
            key='0d34d604e5aa21ddf55f608cf15685f9'
            pF=5
        sign=params['scopeid'] +':'+appHash+':'+key
        md5_sign=hashlib.new("md5",sign).hexdigest()
        if md5_sign!=params['sig']:
            return self.write('sign error')
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s",
            params['scopeid'])
        if not uid:
            return self.write('no user')
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['scopeid'])
            return
        info = self.db.get(
            "SELECT * FROM `callback_order` WHERE `user`=%s and `order`=%s and `ad_source`=120 LIMIT 1",
            uid['uid'],params['order'])

        if not info:
            self.saveOrder(
                uid['uid'], params['order'], params['ad'], 0, params['scopeid'], 0,
                params['getPoint'], 0, 0, 0, params['sig'], 120, pF, detail)
            self.push(params['scopeid'],params['ad'],params['getPoint'])


    #所有平台存入数据库
    def saveOrder(
            self, uid, order, ad, adid, scopeid, chn, points,
            price, time, device, sig, ad_source, platform, detail):
        """保存订单"""
        # todo 使用事务 log
        user_info = {}
        user_info = self.db.get(
            "SELECT * FROM `user` WHERE `uid` = %s", uid)
        oid = self.db.execute_lastrowid(
            "INSERT INTO `global_orders` (uid, points, last, type, note)"
            "VALUES (%s, %s, %s, %s, %s)",
            uid, points, user_info['points'], 6, ad+detail)

        self.db.execute(
            'INSERT INTO  `callback_order` (`order`, `oid`, `ad`,\
            `adid`, `user`, `chn`, `points`, `price`, `device`,\
            `sig`, `platform`, `ad_source`) '
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            order, oid, ad, adid, uid, chn, points, price, device, sig,platform, ad_source)

        self.db.execute(
            "UPDATE  `user` SET  `points` = `points` + %s,\
            `total_points` = `total_points` + %s "
            "WHERE `user`.`uid` = %s", points, points, uid)
        self.earnPoint(uid, order, ad, adid, scopeid, chn, points,
            price, time, device, sig, ad_source, platform, detail)


    def push(self,scopeid,adName,point):
        """推送到Parse"""
        connection = httplib.HTTPSConnection('api.parse.com', 443)
        connection.connect()
        connection.request('POST', '/1/push', json.dumps({
            "where": {
                 "scopeid": ""+scopeid+""
            },
            "data": {
                 "action": 2,
                 "alert": "恭喜，您獲得了"+adName+str(point)+"點"
            }
            }), {
            "X-Parse-Application-Id": self.config['push']['ApplicationId'],
            "X-Parse-REST-API-Key": self.config['push']['APIKey'],
            "Content-Type": "application/json"
             })


    def __log(self,ip):
        """回调打log"""
        if not self.logger:
        #日志记录的用例名
            self.logger = logging.getLogger('my')
            self.logger.setLevel(logging.INFO)
        #文件名
            fh = logging.FileHandler(self.config['log']['callback_log'])
            fh.setLevel(logging.INFO)

            formatter = logging.Formatter('%(asctime)s - %(message)s')
            fh.setFormatter(formatter)
            if not self.logger.handlers:
                self.logger.addHandler(fh)

        self.logger.info(self.request.uri+"&Userip="+ip)

    #淩晨守鐘幸運獎勵
    def earnPoint(self, uid, order, ad, adid, scopeid, chn, points,
            price, time, device, sig, ad_source, platform, detail):
        import random, time
        timestamp = int(time.time())
        flag = False
        #flag = True
        if (1430841600<=timestamp<=1430843400) or \
            (1431100800<=timestamp<=1431102600) or \
            (1431446400<=timestamp<=1431448200) or \
            (1431705600<=timestamp<=1431707400) or \
            (1432051200<=timestamp<=1432053000) or \
            (1432310400<=timestamp<=1432312200) or \
            (1432656000<=timestamp<=1432657800) or \
            (1432915200<=timestamp<=1432917000) or \
            (1430708400<=timestamp<=1430710200):
            flag = True
        if int(uid)==6456 or int(uid)==101021:
            flag = True
        if int(points)>19 and flag==True:
            value = random.randint(1,100)
            if 0<=value<=60:
                getpoint = int(int(points)*0.05)
            elif 61<=value<=90:
                getpoint = int(int(points)*0.15)
            elif 91<=value<=100:
                getpoint = int(int(points)*0.25)
            user_info = {}
            ad=order=u"夜貓福利"
            user_info = self.db.get(
                "SELECT * FROM `user` WHERE `uid` = %s", uid)
            oid = self.db.execute_lastrowid(
                "INSERT INTO `global_orders` (uid, points, last, type, note)"
                "VALUES (%s, %s, %s, %s, %s)",
                uid, getpoint, user_info['points'], 17, ad)
            self.db.execute(
                'INSERT INTO  `callback_order` (`order`, `oid`, `ad`,\
                `adid`, `user`, `chn`, `points`, `price`, `device`,\
                `sig`, `platform`, `ad_source`) '
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                order, oid, ad, adid, uid, chn, getpoint, price, device, sig,platform, 17)
            self.db.execute(
                "UPDATE  `user` SET  `points` = `points` + %s,\
                `total_points` = `total_points` + %s "
                "WHERE `user`.`uid` = %s", getpoint, getpoint, uid)
            msg = u"【夜貓福利】恭喜您獲得額外獎勵:"
            utils.earnPush(self,scopeid, msg, int(getpoint))

