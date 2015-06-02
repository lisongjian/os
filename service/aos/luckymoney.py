#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

配置模块

@author lisongjian

"""
import protocols
import datetime
import random

class LuckyHandler(protocols.JSONBaseHandler):
    """ 红包接口 """

    @protocols.unpack_arguments()
    def get(self):
        # 查询领取红包
        query = int(self.arguments.get('query', 0))
        # language = self.arguments.get('language', 'zh')
        # platform = self.arguments.get('platform')
        used = self.db.execute_rowcount("SELECT `id` FROM `lucky_money`")
        # 线上线下ip获取方式不同
        ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        # ip = self.request.remote_ip
        Alists = []
        got = False
        order = ad = '紅包'
        point = 10
        uid = self.current_user['uid']
        # FIXME 同一ip不能抢红包, 后台控制钱包数量、
        # 开关红包开关
        open = self.db.get("SELECT `values` FROM `options` WHERE `key`='lucky_money'")
        if open['values'] == 0:
            return
        lucky_money_total = self.db.get("SELECT `values` FROM `options` WHERE `key`='lucky_money_total'")['values']
        userinfo = self.db.get(
            "SELECT `id`,`points` FROM `lucky_money` WHERE `uid`=%s or `ip`=%s LIMIT 1",  uid, ip)
        if userinfo:
            got = True
        if (query !=1) and (used<lucky_money_total):
            c = random.randint(1,1000)
            if 0<c<100:
                point=random.randint(10,25)
            elif 100<=c<200:
                point=random.randint(26,45)
            elif 200<=c<450:
                point=random.randint(46,60)
            elif 450<=c<700:
                point=random.randint(61,75)
            elif 700<=c<850:
                point=random.randint(76,90)
            elif 850<=c<950:
                point=random.randint(91,105)
            elif 950<=c<990:
                point=random.randint(106,120)
            elif 990<=c<1000:
                point=random.randint(200)
            if not userinfo:
                self.db.execute(
                    "INSERT INTO `global_orders` (`uid`, `points`, `last`, `type`, `note`, `appType`)"
                    "VALUES (%s, %s, %s, %s, %s, %s)",uid, point, self.current_user['points'], \
                    14, ad, 0)
                self.db.execute(
                    "INSERT INTO `callback_order`(`order`,`ad`,`user`,`platform`,`ad_source`,`points`)"
                    "VALUES(%s,%s,%s,%s,%s,%s)", order,ad,uid,3,14, point)
                self.db.execute("UPDATE `user` SET `points` = `points` + %s WHERE `uid` = %s", point, int(uid))
                self.db.execute(
                    "INSERT INTO `lucky_money`(`uid`,`name`,`ip`,`points`,`time`)"
                    "VALUES(%s,%s,%s,%s,%s)", uid, self.current_user['name'], ip, point, datetime.datetime.now())
                got = True
        if query == 1 or got == True:
            if userinfo:
                got = True
                point = userinfo['points']
            lists = self.db.query(
                "SELECT * FROM `lucky_money` LIMIT 60")
            for List in lists:
                sname = list(List['name'])
                uname = sname[0] + '***' +sname[-1]
                Alists.append({
                    "username": uname,
                    "time": (List['time']-datetime.timedelta(hours=8)),
                    "point": List['points'],
                })
        self.return_result({"total":lucky_money_total, "used":used, "got":got,"point":point,"lists": Alists})


class ActivityHandler(protocols.JSONBaseHandler):
    """ 活动 """

    @protocols.unpack_arguments()
    def get(self):
        uid = self.current_user['uid']
        if not uid:
            return
        get = False
        Lucky = self.db.get(
            "SELECT * FROM `options` WHERE `key` = 'lucky_money'")
        lucky_money_total = self.db.get("SELECT `values` FROM `options` WHERE `key`='lucky_money_total'")['values']
        if Lucky['values'] == 1:
            lucky_money = True
            userinfo = self.db.get(
                "SELECT `id` FROM `lucky_money` WHERE `uid`=%s",  uid)
            used = self.db.execute_rowcount("SELECT `id` FROM `lucky_money`")
            if (not userinfo) and (used<lucky_money_total):
                get = True
        else:
            lucky_money = False
        Game = self.db.get(
            "SELECT * FROM `options` WHERE `key` = 'game'")
        if Game['values'] == 1:
            game = True
        else:
            game = False
        game_points = self.db.get("SELECT `values` FROM `options` WHERE `key`='game_points'")

        self.return_result({
            "lucky_money": lucky_money,
            "game": game,
            "can_get_lucky_money": get,
            "game_consume_point": game_points['values'],
        })
