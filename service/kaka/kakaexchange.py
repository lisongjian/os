#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author cairuitao@gmail.com
#
""" 兑换积分 """

import protocols
import constants
import time,datetime
import logging
import logging.config
import logging.handlers
import httplib,json
import urllib
import utils
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class NewOrderHandler(protocols.JSONBaseHandler):
    """ 兑换商品 """
    autologger = None  # 自动兑换logger handler

    @protocols.unpack_arguments()
    def post(self):
        print 'ip'
        ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1", ip)
        if ip_info:
            return
        goods_id = self.arguments.get('goods_id', "")
        count = int(self.arguments.get('count', ""))
        title = self.arguments.get('title', "")
        address = self.arguments.get('address', "")
        if count <= 0:
            self.return_error(
                constants.ERR_INVALID_GOODS_COUNT,
                "兑换数量必须大于或者等于1")
            return

        # FIXME 这里要用事务
        goods_info = self.db.get(
            "SELECT `goods_id`, `title`, `points`, `price` "
            "FROM `exchange_goods` WHERE `goods_id` = %s",
            goods_id)

        if not goods_info:
            self.return_error(constants.ERR_INVALID_GOODS_ID, "货物编号错误")
            return

        total_points = goods_info['points'] * count

        # 确定用户兑换资格
        # TODO 对于被封杀的用户，应该禁止兑换
        user_info = self.db.get(
            "SELECT * FROM `user` WHERE `uid` = %s",
            self.current_user['uid'])
        #fa = "SELECT * FROM `callback_order` WHERE `ad_source`=112 or `ad_source`=108 or `ad_source`=103 \
        #        AND `ad_source`<>100 AND `ad_source`<>101 AND `ad_source`<>102 AND `ad_source`<>104 \
        #        AND `ad_source`<>105 AND `ad_source`<>106 AND `ad_source`<>107 AND `ad_source`<>109 \
        #        AND `ad_source`<>110 AND `ad_source`<>111 AND `ad_source`<>113"
        if total_points > user_info['points']:
            self.return_error(constants.ERR_NOT_ENOUGH_POINTS, "余额不足")
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid`=%s AND `status`=1 LIMIT 1",self.current_user['uid'])
        if black_user:
            self.__log(0,self.current_user['uid'],self.current_user['scopeid'],0,goods_id,0,title,'作弊不给兑换','',0,0,0)
            return

        # 创建订单流水
        # 增加兑换流水，注意这里是消耗积分，所以是负数
        note = "兑换"+title
        oid = self.db.execute_lastrowid(
            "INSERT INTO `global_orders` (uid, points, last, type, note, appType)"
            "VALUES (%s, %s, %s, %s, %s, 1)",
            self.current_user['uid'], -total_points, user_info['points'], 5, note)

        # 创建货物订单
        self.db.execute(
            "INSERT INTO `exchange_orders` (uid, oid, points, total_points, price, total_price, goods_id, goods_title, count,address, appType)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            self.current_user['uid'], oid, goods_info['points'], total_points,
            goods_info['price'], goods_info['price'] * count,
            goods_id, title, count,address, 1)

        #自动兑换限制每日三次
        ChangeCheat = self.db.get(
            "SELECT count(*) FROM `global_orders` WHERE `uid` = %s AND `type` = 5 AND DATE(`record_time`)=CURDATE()",
            self.current_user['uid'])
        if ChangeCheat:
            if ChangeCheat['count(*)']<3:
                #self.autoChange(goods_id,self.current_user['uid'],oid,self.current_user['scopeid'],title)
                pass
            else:
                msg = "卡卡赚当天兑换超过三次，已停止对该用户自动兑换"
                utils.pushover(self,self.current_user['uid'],title, msg)

        # 更新用户余额
        remain_points = user_info['points'] - total_points
        exchange_points = user_info['ex_points'] + total_points
        self.db.execute(
            "UPDATE `user` SET `points` = %s, `ex_points` = %s WHERE `uid` = %s",
            remain_points, exchange_points, self.current_user['uid'])

        # 增加货物兑换次数标记
        self.db.execute(
            "UPDATE `exchange_goods` SET `exchange_counts` = `exchange_counts` + 1"
            " WHERE `goods_id` = %s",
            goods_id)
        self.return_result({
                    "points": remain_points,
                    })

    #自动兑换
    def autoChange(self,goods_id,user,oid,scopeid,title):
        card = self.db.get(
            "SELECT *,COUNT(*) FROM `exchange_cards` WHERE `goods_id` = %s AND `status`=0 AND `num`!=' ' "
            "ORDER BY `id` LIMIT 1", goods_id)
        #todo 统计卡数 少于则pushover
        if card['COUNT(*)']>0:
            self.db.execute(
            "UPDATE `exchange_orders` SET `num` = %s, `pwd` = %s, `status`=1"
            " WHERE `oid` = %s",
            card['num'], card['pwd'], oid)
            orderid = self.db.get(
                "SELECT `id` FROM `exchange_orders` WHERE `oid`= %s ", oid)
            now = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
            print 'now'+str(now)
            self.db.execute(
            "UPDATE `exchange_cards` SET `status`=1, `uid` = %s, `changetime` = %s WHERE `id`=%s", user, now, card['id'])
            #if card['COUNT(*)']>0:
            self.__log(oid,user,scopeid,card['id'],card['goods_id'],card['type_id'],card['title'],card['num'],card['pwd'],card['inprice'],card['outprice'],orderid['id'])
            self.push(scopeid,card['title'])
            if goods_id == "16":
                cardNum = self.db.get("SELECT * FROM `options` WHERE `key` = 'mycard50'")
                if card['COUNT(*)']<cardNum['values']:
                    self.pushover(title, card['COUNT(*)']-1)
            elif goods_id == "31":
                cardNum = self.db.get("SELECT * FROM `options` WHERE `key` = 'gash50'")
                if card['COUNT(*)']<cardNum['values']:
                    self.pushover(title, card['COUNT(*)']-1)
            elif goods_id == "28":
                cardNum = self.db.get("SELECT * FROM `options` WHERE `key` = 'mycardline60'")
                if card['COUNT(*)']<cardNum['values']:
                    self.pushover(title, card['COUNT(*)']-1)
            elif goods_id == "36":
                cardNum = self.db.get("SELECT * FROM `options` WHERE `key` = 'beikebi140'")
                if card['COUNT(*)']<cardNum['values']:
                    self.pushover(title, card['COUNT(*)']-1)
            elif goods_id == "37":
                cardNum = self.db.get("SELECT * FROM `options` WHERE `key` = 'youe150'")
                if card['COUNT(*)']<cardNum['values']:
                    self.pushover(title, card['COUNT(*)']-1)
            elif goods_id == "17":
                cardNum = self.db.get("SELECT * FROM `options` WHERE `key` = 'mycard150'")
                if card['COUNT(*)']<cardNum['values']:
                    self.pushover(title, card['COUNT(*)']-1)
            elif goods_id == "35":
                cardNum = self.db.get("SELECT * FROM `options` WHERE `key` = 'beikebi100'")
                if card['COUNT(*)']<cardNum['values']:
                    self.pushover(title, card['COUNT(*)']-1)
            elif goods_id == "61":
                cardNum = self.db.get("SELECT * FROM `options` WHERE `key` = 'amazon'")
                if card['COUNT(*)']<cardNum['values']:
                    self.pushover(title, card['COUNT(*)']-1)
            elif goods_id == "26":
                cardNum = self.db.get("SELECT * FROM `options` WHERE `key` = 'lajiaoka50'")
                if card['COUNT(*)']<cardNum['values']:
                    self.pushover(title, card['COUNT(*)']-1)
            elif goods_id == "18":
                cardNum = self.db.get("SELECT * FROM `options` WHERE `key` = 'mycard300'")
                if card['COUNT(*)']<cardNum['values']:
                    self.pushover(title, card['COUNT(*)']-1)
            else:
                cardNum = self.db.get("SELECT * FROM `options` WHERE `key` = 'card'")
                if card['COUNT(*)']<cardNum['values']:
                    self.pushover(title, card['COUNT(*)']-1)
        else:
            self.pushover(title, card['COUNT(*)']-1)


    def __log(self,oid,user,scopeid,id,goods_id,type_id,title,num,pwd,inprice,outprice,orderid):
        """自动兑换打log"""
        if not self.autologger:
            self.autologger = logging.getLogger('automy')
            self.autologger.setLevel(logging.INFO)
            autofh = logging.FileHandler(self.config['log']['autoChange_log'])
            autofh.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(message)s')
            autofh.setFormatter(formatter)
            if not self.autologger.handlers:
                self.autologger.addHandler(autofh)
            self.autologger.info("kakaoid="+str(oid)+"&user="+str(user)+"&scopeid="+scopeid+
                             "&cardid="+str(id)+"&goods_id="+str(goods_id)+"&type_id="+str(type_id)+
                             "title="+title+"&num="+num+"&pwd="+pwd+"&inprice="+str(inprice)+"&outprice="+str(outprice)+"&orderid="+str(orderid))

    def push(self,scopeid,title):
        """推送到Parse"""
        connection = httplib.HTTPSConnection('api.parse.com', 443)
        connection.connect()
        connection.request('POST', '/1/push', json.dumps({
            "where": {
                 "deviceType": "android",
                 "scopeid": ""+scopeid+""
            },
            "data": {
                 "action": 1,
                 "alert": "恭喜，"+title.encode("utf-8")+"兌換成功了。點擊查看兌換碼"
            }
            }), {
            "X-Parse-Application-Id": self.config['kakapush']['ApplicationId'],
            "X-Parse-REST-API-Key": self.config['kakapush']['APIKey'],
            "Content-Type": "application/json"
             })

    def pushover(self,title, num):
        """推送到Pushover"""
        conn = httplib.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
            urllib.urlencode({
                "token": "apdAUUmA7SzJnkruZTadPeuGTk3RV2",
                "user": "udS2Sm64GcdsUAUyM16nfw592B7gAC",
                "message": title+"只剩"+str(num)+"，请及时进货",
            }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()


class DuibaUrlHandler(protocols.JSONBaseHandler):
        """ 兑吧免登陆url """

        @protocols.unpack_kakaarguments_byscopeid()
        def get(self):

            timestamp = int(time.time() * 1000)
            uid = self.current_user['uid']
            points = self.current_user['points']
            appKey = self.config['duiba']['appKey']
            appSecret = self.config['duiba']['appSecret']
            params = {'uid': uid, 'credits': points, 'appSecret': appSecret, \
                    'appKey': appKey, 'timestamp': timestamp}
            sign = utils.md5_sign(params)
            duiba = self.db.get("SELECT `values` FROM `options` WHERE `key` = 'duiba'")
            url = None
            if duiba['values'] == 1:
                url = "http://www.duiba.com.cn/autoLogin/autologin?uid=%s&credits=%s&appKey=%s&sign=%s&timestamp=%s" \
                        % (uid, points, appKey, sign, timestamp)
            elif duiba['values'] == 0:
                url = None
            self.return_result({"url": url})


class ListGoodsHandler(protocols.JSONBaseHandler):
    """ 获取可兑换货物列表 """

    @protocols.unpack_arguments(with_scopeid=False)
    def get(self):
        tid = self.arguments.get('cid', "")
        types = self.db.query("SELECT * FROM `exchange_types` WHERE `tid`=%s AND `code`=0", tid)

        formated_goods_list = []
        for typ in types:
            formated_goods_list.append({
                "title": typ['title'],
                'icon': self.config['goods']['static_url'] + typ['icon'],
                "tid":typ['id'],
                "list": self.get_goods(typ['id']),
            })

        self.return_result({"goods": formated_goods_list})

    def get_goods(self, type_id):
        goods = self.db.query(
            "SELECT * FROM `exchange_goods` WHERE `type_id` = %s and `status`=1", type_id)
        formated_goods_list = []
        for item in goods:
            formated_item = {
                'gid': item['goods_id'],
                'price': item['points'],
                'title': item['title'],
                 #'desc': item['description'],
                 #'exchange_counts': item['exchange_counts'],
            }
            formated_goods_list.append(formated_item)
        return formated_goods_list


class MyOrdersHandler(protocols.JSONBaseHandler):
    """ 获取我的订单列表 """

    order_status = {
        0: "待审核",
        1: "审核通过",
        2: "忽略（非法）",
        3: "延缓"
    }

    @protocols.unpack_kakaarguments_byscopeid()
    def get(self):
        orders = self.db.query(
            "SELECT * FROM `exchange_orders` WHERE `uid` = %s ORDER BY `create_time` DESC ",
            self.current_user['uid'])

        print self.current_user['uid']
        if not orders:
            self.return_result({"orders": []})
            return

        formated_orders_list = []
        for item in orders:
            if item['goods_id']==64 or item['goods_id']==65 or item['goods_id']==66 \
                    or item['goods_id']==89 or item['goods_id']==90 or item['goods_id']==91 \
                    or item['goods_id']==92 or item['goods_id']==93 or item['goods_id']==94 \
                    or item['goods_id']==95 or item['goods_id']==96:
                formated_item = {
                    'oid': item['id'],
                    'status': item['status'],
                    'title':item['goods_title'].encode('utf-8'),
                    'notes': item['notes'],
                    'create_time': time.mktime(item['create_time'].timetuple()),
                    'score': item['total_points'],
                    'uid': item['num'],
                }
                formated_orders_list.append(formated_item)
            else:
                formated_item = {
                    'oid': item['id'],
                    'status': item['status'],
                    'title':item['goods_title'].encode('utf-8'),
                    'notes': item['notes'],
                    'create_time': time.mktime(item['create_time'].timetuple()),
                    'score': item['total_points'],
                    'code' : item['num'],
                    'pwd': item['pwd'],
                }
                formated_orders_list.append(formated_item)
            #print formated_orders_list

        self.return_result({"orders": formated_orders_list})


class LatestOrdersHandler(protocols.JSONBaseHandler):
    """" 最新兑换记录50条 """

    @protocols.unpack_kakaarguments_byscopeid()
    def get(self):
        orders = self.db.query(
            "SELECT `uid`, `goods_title`, `count`, `create_time` FROM `exchange_orders` "
            "WHERE `status`=1 ORDER BY `create_time` DESC LIMIT 50")

        if not orders:
            self.return_result({"orders": []})
            return

        formated_orders_list = []
        for item in orders:
            formated_item = {
                'uid': item['uid'],
                'title': item['goods_title'].encode('utf-8'),
                'count': item['count'],
                'create_time': time.mktime(item['create_time'].timetuple()),
            }
            formated_orders_list.append(formated_item)

        self.return_result({"orders": formated_orders_list})
