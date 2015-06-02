#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

广告平台回调处理
@author zhenyong

"""

from protocols import JSONBaseHandler
import datetime
import time as mtime
import logging
import logging.config


class CallbackHandler(JSONBaseHandler):

    logger = None  # logger handler

    def get(self, platform):
        """接收广告平台回调"""
        self.__log()
        if 'youmiios' == platform:
            self.__save_youmi_ios_order()
        elif 'youmiaos' == platform:
            self.__save_youmi_aos_order()
        elif 'wanpuaos' == platform:
            self.__save_wanpu_aos_order()
        elif 'duomengios' == platform:
            self.__save_duomeng_ios_order()
        elif 'dianruios' == platform:
            self.__save_dianru_ios_order()
        elif 'midiios' == platform:
            self.__save_midi_ios_order()
        elif 'anwoios' == platform:
            self.__save_anwo_ios_order()
        elif 'chukongios' == platform:
            self.__save_chukong_ios_order()

        self.write('ok')

    def __save_youmi_ios_order(self):
        """有米iOS订单"""
        order = self.get_argument('order', None)
        # app = self.get_argument('app', None)
        ad = self.get_argument('ad', None)
        adid = self.get_argument('adid', None)
        user = self.get_argument('user', None)
        chn = self.get_argument('chn', None)
        points = self.get_argument('points', None)
        price = self.get_argument('price', None)
        time = self.get_argument('time', None)
        # 格式化
        time = datetime.datetime.utcfromtimestamp(
            int(time)).strftime("%Y-%m-%d %H:%M:%S")
        device = self.get_argument('device', None)
        sig = self.get_argument('sig', None)
        self.saveOrder(
            order, ad, adid, user, chn,
            points, price, time, device, sig, 1)

    def __save_youmi_aos_order(self):
        """有米aos订单"""
        order = self.get_argument('order', None)
        # app = self.get_argument('app', None)
        ad = self.get_argument('ad', None)
        adid = self.get_argument('adid', None)
        user = self.get_argument('user', None)
        chn = self.get_argument('chn', None)
        points = self.get_argument('points', None)
        price = self.get_argument('price', None)
        time = self.get_argument('time', None)
        # 格式化
        time = datetime.datetime.utcfromtimestamp(
            int(time)).strftime("%Y-%m-%d %H:%M:%S")
        device = self.get_argument('device', None)
        sig = self.get_argument('sig', None)
        self.saveOrder(
            order, ad, adid, user, chn,
            points, price, time, device, sig, 1)

    def __save_wanpu_aos_order(self):
        """万普aos订单"""
        user = self.get_argument('key', None)
        device = self.get_argument('udid', None)
        points = self.get_argument('points', None)
        price = self.get_argument('bill', None)
        ad = self.get_argument('ad_name', None)
        advid = self.get_argument('adv_id', None)
        time = mtime.strftime(
            "%Y-%m-%d %H:%M:%S",
            mtime.localtime(mtime.time()))
        order = 'wanpu_' + advid + user
        self.saveOrder(
            order, ad, 0, user, 0,
            points, price, time, device, '', 3)

    def __save_duomeng_ios_order(self):
        """多盟ios订单"""
        order = self.get_argument('orderid', None)
        order = 'duomeng_' + order
        ad = self.get_argument('ad', None)
        adid = self.get_argument('adid', None)
        user = self.get_argument('user', None)
        device = self.get_argument('device', None)
        chn = self.get_argument('channel', 0)
        price = self.get_argument('price', None)
        points = self.get_argument('point', None)
        time = self.get_argument('ts', None)
        # 格式化
        time = datetime.datetime.utcfromtimestamp(
            int(time)).strftime("%Y-%m-%d %H:%M:%S")
        self.saveOrder(
            order, ad, adid, user, chn,
            points, price, time, device, '', 2)

    def __save_limei_ios_order(self):
        """力美ios订单"""
        order = self.get_argument('orderId', None)
        order = 'limei_' + order
        ad = self.get_argument('title', None)
        #adid = self.get_argument('cid', None)
        user = self.get_argument('aid', None)
        device = self.get_argument('uid', None) \
            + self.get_argument('aid', None)
        points = self.get_argument('point', None)

    def __save_dianru_ios_order(self):
        """点入ios订单"""
        order = self.get_argument('hashid', None)
        order = 'dianru_' + order
        ad = self.get_argument('adname', None)
        adid = self.get_argument('adid', None)
        user = self.get_argument('userid', None)
        device = self.get_argument('deviceid', None)
        chn = self.get_argument('source', 0)
        points = self.get_argument('point', None)
        time = self.get_argument('time', None)
        # 格式化
        time = datetime.datetime.utcfromtimestamp(
            int(time)).strftime("%Y-%m-%d %H:%M:%S")
        self.saveOrder(
            order, ad, adid, user, chn,
            points, None, time, device, '', 4)

    def __save_midi_ios_order(self):
        """米迪ios订单"""
        order = self.get_argument('trand_no', None)
        order = 'midi_' + order
        ad = self.get_argument('appName', None)
        adid = self.get_argument('id', None)
        points = self.get_argument('cash', None)
        device = self.get_argument('imei', None)
        # 下载应用安装包名
        # bundleid = self.get_argument('bundleId', None)
        user = self.get_argument('param0', None)
        sig = self.get_argument('sign', None)
        self.saveOrder(
            order, ad, adid, user, 0,
            points, None, None, device, sig, 5)

    def __save_anwo_ios_order(self):
        """安沃ios订单"""
        idfa = self.get_argument('idfa', None)
        # 时间戳 13位
        time = self.get_argument('ts', None)
        # 通过时间，idfa来判别订单唯一
        order = 'anwo_' + time[3:10] + idfa[-12:]
        ad = self.get_argument('adname', None)
        adid = self.get_argument('adid', None)
        points = self.get_argument('point', None)
        user = self.get_argument('keyword', None)
        # 测试发现device的值为空
        # device = self.get_argument('device', None)
        # 格式化
        time = datetime.datetime.utcfromtimestamp(
            int(time[0:10])).strftime("%Y-%m-%d %H:%M:%S")
        sig = self.get_argument('sign', None)
        self.saveOrder(
            order, ad, adid, user, 0,
            points, None, time, idfa, sig, 6)

    def __save_chukong_ios_order(self):
        """触控ios订单"""
        order = self.get_argument('transactionid', None)
        order = 'chukong_' + order
        ad = self.get_argument('adtitle', None)
        adid = self.get_argument('adid', None)
        idfa = self.get_argument('idfa', None)
        # mac = self.get_argument('mac', None)
        user = self.get_argument('token', None)
        points = self.get_argument('coins', None)
        sig = self.get_argument('sign', None)
        self.saveOrder(
            order, ad, adid, user, 0,
            points, None, None, idfa, sig, 7)

    def saveOrder(
            self, order, ad, adid, user, chn, points,
            price, time, device, sig, ad_source):
        """保存订单"""
        # todo 使用事务 log
        user_info = self.db.get(
            "SELECT `points` FROM `user` WHERE `uid` = %s",
            user)

        oid = self.db.execute_lastrowid(
            "INSERT INTO `global_orders` (uid, points, last)"
            "VALUES (%s, %s, %s)",
            user, points, user_info['points'])

        self.db.execute(
            'INSERT INTO  `callback_order` (`order`, `oid`, `ad`,\
            `adid`, `user`, `chn`, `points`, `price`, `time`, `device`,\
            `sig`, `platform`, `ad_source`) '
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 5, %s)",
            order, oid, ad, adid, user, chn, points, price, time, device, sig, ad_source)

        self.db.execute(
            "UPDATE  `you1000`.`user` SET  `points` = `points` + %s,\
            `total_points` = `total_points` + %s "
            "WHERE `user`.`uid` = %s", points, points, user)

    def __log(self):
        """回调打log"""
        if not self.logger:
            self.logger = logging.getLogger('my')
            self.logger.setLevel(logging.INFO)

            fh = logging.FileHandler(self.config['log']['callback_log'])
            fh.setLevel(logging.INFO)

            formatter = logging.Formatter('%(asctime)s - %(message)s')
            fh.setFormatter(formatter)
            if not self.logger.handlers:
                self.logger.addHandler(fh)

        self.logger.info(self.request.uri)
