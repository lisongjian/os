#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

用户相关
@author zhenyong

"""

import protocols
import hashlib
import constants
import time


class UserHandler(protocols.JSONBaseHandler):
    """ 用户创建以及信息查询 """

    @protocols.unpack_arguments(with_token=False)
    def post(self):
        # H7hLcmuAhCZOZYT2zJTv6+ouY9Wtu+RomKkaaMrBG2MWouL9YixIC/LrVf6ekk8v
        params = {}
        for key in ['ei', 'si', 'andid', 'mac', 'andid',
                    'idfa', 'idfv', 'udid', 'rt']:
            params[key] = self.arguments.get(key, "")

        fingerprinting = self.__get_devicefingerprinting(params)

        user_device = self.db.get(
            "SELECT `uid`, `fingerprinting` from `user_device` \
            where `fingerprinting` = %s",
            fingerprinting)

        if not user_device:
            if params['ei']:
                platform = 3
            else:
                platform = 5

            # 新增一个uid
            uid = self.db.execute_lastrowid(
                "INSERT INTO `user_device` (`ei`, `si`, `mac`, `andid`,\
                `idfa`, `idfv`, `udid`, `platform`, `fingerprinting`) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                params['ei'], params['si'], params['mac'], params['andid'],
                params['idfa'], params['idfv'], params['udid'],
                platform, fingerprinting)

            self.db.execute(
                "INSERT INTO `user` (`uid`)"
                "VALUES (%s)",
                uid)
            user_info = {'uid': uid, 'points': 0}
        else:
            # 已有uid
            user_info = self.db.get(
                "SELECT * FROM `user` WHERE `uid` = %s",
                user_device['uid'])

        self.return_result({
            "uid": user_info['uid'],
            "points": user_info['points'],
            "token": self.gen_token(user_info['uid'])})

    def __get_devicefingerprinting(self, device_params):
        """简单的生成设备指纹方法"""
        valid_params = [
            device_params['ei'],
            device_params['si'],
            device_params['mac'],
            device_params['andid'],
            device_params['idfa'],
        ]
        device_str = ':'.join(str(valid_params))
        return hashlib.md5(device_str).hexdigest()


class PointsHandler(protocols.JSONBaseHandler):
    """ 用户积分、等级、签到天数 """

    @protocols.unpack_arguments()
    def get(self):
        ex_rate = self.db.get("SELECT * FROM `options` WHERE `key`='exchange_rate'")
        points = dict(
            points=self.current_user['points'],
            ex_points=self.current_user['ex_points'],
            ex_price=float(self.current_user['ex_points'])/float(ex_rate['values']),
            invite_points=self.current_user['invite_points'],
            total_points=self.current_user['total_points'],
            grade=self.current_user['grade'],
            days=self.current_user['sign_days'],
            invite_num=self.current_user['invites'],
        )
        self.return_result(points)


class PointsDetailHandler(protocols.JSONBaseHandler):
    """ 用户积分流水 """

    @protocols.unpack_arguments()
    def get(self):
        # d8iD0rnprIwYnYLHWACYciNejLEFTznTHP8B6+0VsoH90m15C7973Vywn
        # rkHJRrUNxAxgjDeswK5LLIR3208tpunHdqZWY6ce1mYYqPH/HA=
        print self.current_user['uid']
        orders = self.db.query(
            "SELECT * FROM `callback_order` WHERE `user` = %s",
            self.current_user['uid'])

        records = []
        for order in orders:
            records.append({
                'oid': order['id'],
                'status': '已完成',
                'title': '安装' + order['ad'].encode('utf-8'),
                'notes': '获取' + str(order['points']) + '砖石',
                'points': order['points'],
                'create_time': order['time']})

        self.return_result({"records": records})


class SignHandler(protocols.JSONBaseHandler):
    """ 用户签到 """

    @protocols.unpack_arguments()
    def get(self):
        tmp = self.db.get("SELECT * FROM `options` WHERE `key` = 'sign_prize'")
        sign_prize = tmp['values']
        timestamp = self.arguments.get("rt")
        sign_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timestamp)))
        # 检查用户当天是否已经签到
        flag = self.db.get(
            "SELECT `id` FROM `user_sign` WHERE `uid`=%s AND DATE(`time`)=CURDATE()",
            self.current_user['id'])
        if flag:
            self.return_error(constants.ERR_REPEAT_SIGN)
            return

        sign_days = self.current_user['sign_days'] + 1
        grade = sign_days / 5 + 1
        if grade > self.current_user['grade']:
            levelup = 1
        else:
            levelup = 0

        # 插入签到记录
        self.db.execute(
            "INSERT INTO `user_sign`(`uid`, `time`, `grade`)"
            "VALUES(%s, %s, %s)", self.current_user['id'], sign_time, grade)

        # 更新用户信息
        self.db.execute(
            "UPDATE `user` SET `points` = `points` + %s, \
            `total_points` = `total_points` + %s, `sign_days` = %s, `grade` = %s "
            "WHERE `uid` = %s", sign_prize, sign_prize, sign_days, grade, self.current_user['id'])
        sign = dict(
            points=self.current_user['points']+sign_prize,
            grade=grade,
            days=sign_days,
            levelup=levelup,
        )
        self.return_result({"sign": sign})


class LevelHandler(protocols.JSONBaseHandler):
    """ 等级奖励信息 """

    @protocols.unpack_arguments()
    def get(self):
        prizes = self.db.query("SELECT * FROM `level_prize`")
        self.return_result({"prizes": prizes})


class LevelUpHandler(protocols.JSONBaseHandler):
    """ 根据用户等级领取奖励 """

    @protocols.unpack_arguments()
    def get(self):
        level = self.arguments.get("level")
        # 判断用户等级是否足够领奖
        if level < self.current_user['grade']:
            self.return_error(constants.ERR_NOT_ENOUGH_GRADE)
            return

        # 判断用户是否重复领奖
        flag = self.db.get(
            "SELECT `id` FROM `level_prize_re` "
            "WHERE `uid` = %s AND `level` = %s",
            self.current_user['id'], level)
        if flag:
            self.return_error(constants.ERR_REPEAT_AWARD)
            return

        level_prize = self.db.get(
            "SELECT * FROM `level_prize`"
            "WHERE `level` = %s", level)
        self.db.execute(
            "UPDATE `user` SET `points` = `points` + %s, `total_points` = `total_points` + %s"
            "WHERE `uid` = %s", level_prize['prize'], level_prize['prize'], self.current_user['id'])
        self.db.execute(
            "INSERT INTO `level_prize_re`(`uid`, `level`, `prize`)"
            "VALUES(%s, %s, %s)", self.current_user['id'], level, level_prize['prize'])
        self.return_success()


class TodayHandler(protocols.JSONBaseHandler):
    """ 用户当天数据 """

    @protocols.unpack_arguments()
    def get(self):
        uid = self.current_user['id']
        # 已兑换收益
        exchange = self.db.get(
            "SELECT SUM(`total_points`) AS data FROM `exchange_orders` "
            "WHERE `uid` = %s AND DATE(`create_time`) = CURDATE()", uid)
        if not exchange['data']:
            exchange['data'] = 0
        # 任务收益
        callback = self.db.get(
            "SELECT SUM(`points`) AS data FROM `callback_order` "
            "WHERE `user` = %s AND DATE(`time`) = CURDATE()", uid)
        if not callback['data']:
            callback['data'] = 0
        # 签到收益
        sign = self.db.get(
            "SELECT `id` FROM `user_sign` "
            "WHERE `uid` = %s AND DATE(`time`) = CURDATE()", uid)
        if sign:
            sign_points = 200
        else:
            sign_points = 0
        # 等级提升收益
        level_up = self.db.get(
            "SELECT SUM(`prize`) AS data FROM `level_prize_re` "
            "WHERE `uid` = %s AND DATE(`time`) = CURDATE()", uid)
        if not level_up['data']:
            level_up['data'] = 0
        # 邀请收益
        invite = self.db.get(
            "SELECT SUM(`prize`) AS data FROM `invite_prize` "
            "WHERE `uid` = %s AND DATE(`time`) = CURDATE()", uid)
        if not invite['data']:
            invite['data'] = 0

        total = callback['data'] + sign_points + level_up['data'] + invite['data']
        today = dict(
            total=total,
            task=callback['data'],
            sign=sign_points,
            level=level_up['data'],
            invite=invite['data'],
        )
        self.return_result({"today": today})


class NewUserHandler(protocols.JSONBaseHandler):
    """ 新用户领奖 """

    @protocols.unpack_arguments()
    def get(self):
        if not self.current_user['new']:
            self.return_error(constants.ERR_NOT_NEW_USER)
            return

        new_user = self.db.get("SELECT * FROM `options` WHERE `key` = 'new_user'")
        prize = int(new_user['values'])
        self.db.execute(
            "UPDATE `user` SET `points` = `points` + %s, `total_points` = `total_points` + %s, \
            `new` = 0 WHERE `uid` = %s", prize, prize, self.current_user['id'])
        self.db.execute(
            "INSERT INTO `global_orders`(uid, points, last)VALUES(%s, %s, %s)",
            self.current_user['id'], prize+self.current_user['points'], self.current_user['points'])
        self.return_success()
