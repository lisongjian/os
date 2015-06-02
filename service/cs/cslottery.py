#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: chenjiehua@youmi.net, lisongjian@youmi.net
#

"""抽奖小游戏

"""
import random
import protocols
import constants

class BigSmallHandler(protocols.JSONBaseHandler):
    """ 抽大小 """

    @protocols.unpack_csarguments_byscopeid()
    def post(self):
        game_points = self.db.get("SELECT `values` FROM `options` WHERE `key` = 'game_points'")['values']
        if self.current_user['points'] < game_points:
            self.return_error(constants.ERR_NOT_ENOUGH_POINTS)
            return
        order = ad = u'抽大小'
        game_open = self.db.get("SELECT `values` FROM `options` WHERE `key` = 'game'")['values']
        if game_open == 0:
            return
        uid = self.current_user['uid']
        self.db.execute(
            "INSERT INTO `global_orders` (`uid`, `points`, `last`, `type`, `note`, `appType`)"
            "VALUES (%s, %s, %s, %s, %s, %s)",uid, -game_points, self.current_user['points'], \
            13, ad, 0)
        self.db.execute(
            "INSERT INTO `callback_order`(`order`,`ad`,`user`,`platform`,`ad_source`,`points`)"
            "VALUES(%s,%s,%s,%s,%s,%s)", order,ad,uid,3,13,-game_points)
        c = random.randint(0, 9)
        status = 0
        prize = 0
        if c == 1 or c == 3:
            status = 1
            prize = 250
            self.new_global_order(
                uid, 250, self.current_user['points'], \
                13, ad, 0
            )
            self.db.execute(
                "INSERT INTO `callback_order`(`order`,`ad`,`user`,`platform`,`ad_source`,`points`)"
                "VALUES(%s,%s,%s,%s,%s,%s)", order,ad,uid,3,13,250)
            self.db.execute("UPDATE `user` SET `points` = `points` + %s WHERE `uid` = %s", 250-game_points, uid)
        else:
            status = 0
            prize = 0
            self.db.execute("UPDATE `user` SET `points` = `points` - %s WHERE `uid` = %s", 100, int(uid))
        d = {
            "status": status,
            "prize": prize,
        }
        self.return_result(d)

    def add_total_points(self, uid, points):
        return self.db.execute(
            "UPDATE `user` SET `points` = `points` + %s", \
            "WHERE `uid` = %s", int(points), int(uid))

    def new_global_order(self, uid, points, last, typ, note, appType):
        return self.db.execute(
            "INSERT INTO `global_orders` (`uid`, `points`, `last`, `type`, `note`, `appType`)"
            "VALUES (%s, %s, %s, %s, %s, %s)", uid, points, last, typ, note, appType)


class ScratchCardHandler(protocols.JSONBaseHandler):
    """ 刮刮卡 """

    @protocols.unpack_csarguments_byscopeid()
    def post(self):
        game_points = self.db.get("SELECT `values` FROM `options` WHERE `key` = 'game_points'")['values']
        if self.current_user['points'] < game_points:
            self.return_error(constants.ERR_NOT_ENOUGH_POINTS)
            return
        game_open = self.db.get("SELECT `values` FROM `options` WHERE `key` = 'game'")['values']
        if game_open == 0:
            return
        order = ad = u'刮刮卡'
        uid = self.current_user['uid']
        self.db.execute(
            "INSERT INTO `global_orders` (`uid`, `points`, `last`, `type`, `note`, `appType`)"
            "VALUES (%s, %s, %s, %s, %s, %s)",uid, -game_points, self.current_user['points'], \
            13, ad, 0)
        self.db.execute(
            "INSERT INTO `callback_order`(`order`,`ad`,`user`,`platform`,`ad_source`,`points`)"
            "VALUES(%s,%s,%s,%s,%s,%s)", order,ad,uid,3,13,-game_points)
        c = random.randint(0, 99)
        status = 0
        prize = 25
        if 0<=c<5:
            status = 1
            prize = random.randint(120,150)
            self.db.execute(
                "INSERT INTO `global_orders` (`uid`, `points`, `last`, `type`, `note`, `appType`)"
                "VALUES (%s, %s, %s, %s, %s, %s)",uid, prize, self.current_user['points'], \
                13, ad, 0)
            self.db.execute(
                "INSERT INTO `callback_order`(`order`,`ad`,`user`,`platform`,`ad_source`,`points`)"
                "VALUES(%s,%s,%s,%s,%s,%s)", order,ad,uid,3,13,prize)
            self.db.execute("UPDATE `user` SET `points` = `points` + %s WHERE `uid` = %s", prize-game_points, int(uid))
        elif 5<=c<25:
            status = 0
            prize = random.randint(90,100)
            self.new_global_order(
                uid, prize, self.current_user['points'], \
                13, ad, 0
            )
            self.db.execute(
                "INSERT INTO `callback_order`(`order`,`ad`,`user`,`platform`,`ad_source`,`points`)"
                "VALUES(%s,%s,%s,%s,%s,%s)", order,ad,uid,3,13,prize)
            self.db.execute("UPDATE `user` SET `points` = `points` - %s WHERE `uid` = %s", (game_points-prize), int(uid))
        elif 25<=c<50:
            status = 0
            prize = random.randint(70,90)
            self.new_global_order(
                uid, prize, self.current_user['points'], \
                13, ad, 0
            )
            self.db.execute(
                "INSERT INTO `callback_order`(`order`,`ad`,`user`,`platform`,`ad_source`,`points`)"
                "VALUES(%s,%s,%s,%s,%s,%s)", order,ad,uid,3,13,prize)
            self.db.execute("UPDATE `user` SET `points` = `points` - %s WHERE `uid` = %s", (game_points-prize), int(uid))
        elif 50<=c<80:
            status = 0
            prize = random.randint(50,70)
            self.new_global_order(
                uid, prize, self.current_user['points'], \
                13, ad, 0
            )
            self.db.execute(
                "INSERT INTO `callback_order`(`order`,`ad`,`user`,`platform`,`ad_source`,`points`)"
                "VALUES(%s,%s,%s,%s,%s,%s)", order,ad,uid,3,13,prize)
            self.db.execute("UPDATE `user` SET `points` = `points` - %s WHERE `uid` = %s", (game_points-prize), int(uid))
        elif 80<=c<100:
            status = 0
            prize = random.randint(30,50)
            self.new_global_order(
                uid, prize, self.current_user['points'], \
                13, ad, 0
            )
            self.db.execute(
                "INSERT INTO `callback_order`(`order`,`ad`,`user`,`platform`,`ad_source`,`points`)"
                "VALUES(%s,%s,%s,%s,%s,%s)", order,ad,uid,3,13,prize)
            self.db.execute("UPDATE `user` SET `points` = `points` - %s WHERE `uid` = %s", (game_points-prize), int(uid))

        d = {
            "status": status,
            "prize": prize,
        }
        self.return_result(d)

    def new_global_order(self, uid, points, last, typ, note, appType):
        return self.db.execute(
            "INSERT INTO `global_orders` (`uid`, `points`, `last`, `type`, `note`, `appType`)"
            "VALUES (%s, %s, %s, %s, %s, %s)", uid, points, last, typ, note, appType)
    def add_total_points(self, uid, points):
        return self.db.execute(
            "UPDATE `user` SET `points` = `points` + %s", \
            "WHERE `uid` = %s", int(points), int(uid))

class RoundHandler(protocols.JSONBaseHandler):
    """ 大转盘 """

    @protocols.unpack_csarguments_byscopeid()
    def post(self):
        game_points = self.db.get("SELECT `values` FROM `options` WHERE `key` = 'game_points'")['values']
        if self.current_user['points'] < game_points:
            self.return_error(constants.ERR_NOT_ENOUGH_POINTS)
            return
        game_open = self.db.get("SELECT `values` FROM `options` WHERE `key` = 'game'")['values']
        if game_open == 0:
            return
        order = ad = u'大轉盤'
        uid = self.current_user['uid']
        self.db.execute(
            "INSERT INTO `global_orders` (`uid`, `points`, `last`, `type`, `note`, `appType`)"
            "VALUES (%s, %s, %s, %s, %s, %s)",uid, -game_points, self.current_user['points'], \
            13, ad, 0)
        self.db.execute(
            "INSERT INTO `callback_order`(`order`,`ad`,`user`,`platform`,`ad_source`,`points`)"
            "VALUES(%s,%s,%s,%s,%s,%s)", order,ad,uid,3,13,-game_points)
        c = random.randint(0, 99)
        # 谢谢参与
        if 0 <= c < 30:
            prize = 1
            points = 0
        # 50积分
        elif 30 <= c <80:
            prize = 2
            points = 50
        # 150积分
        elif 80 <= c <90:
            prize = 3
            points = 150
        # 250积分
        elif 90 <= c <98:
            prize = 4
            points = 250
        # 7-11现金券
        elif 98 <= c <99:
            # prize = 4
            pass
        # 全家现金券
        elif 99 <=c <100:
            # prize = 5
            pass
        if 0<=c<98:
            self.new_global_order(
                uid, points, self.current_user['points'], \
                13, ad, 0
            )
            self.db.execute(
                "INSERT INTO `callback_order`(`order`,`ad`,`user`,`platform`,`ad_source`,`points`)"
                "VALUES(%s,%s,%s,%s,%s,%s)", order,ad,uid,3,13,points)
            self.db.execute("UPDATE `user` SET `points` = `points` + %s WHERE `uid` = %s", points-game_points, int(uid))
        d = {
            "prize": prize,
        }
        self.return_result(d)

    def new_global_order(self, uid, points, last, typ, note, appType):
        return self.db.execute(
            "INSERT INTO `global_orders` (`uid`, `points`, `last`, `type`, `note`, `appType`)"
            "VALUES (%s, %s, %s, %s, %s, %s)", uid, points, last, typ, note, appType)
    def add_total_points(self, uid, points):
        return self.db.execute(
            "UPDATE `user` SET `points` = `points` + %s", \
            "WHERE `uid` = %s", int(points), int(uid))
