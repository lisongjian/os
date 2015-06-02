#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author cairuitao@gmail.com, lisongjian@youmi.net
#
""" 主要逻辑 """

import torndb
import tornado.web
import os.path
from protocols import JSONBaseHandler
from service.aos import  callback, user, exchange, config, feedback, invite, duiba, \
        selfurl, callback1, adurl, lottery, luckymoney, luckymoney1, callback2
from service.kaka import  kakacallback, kakauser, kakaexchange, kakaconfig, \
        kakafeedback, kakainvite, kakaduiba, kakaselfurl, kakaadurl
from service.cs import  cscallback, csuser, csexchange, csconfig, csfeedback, csinvite, csduiba, \
        csselfurl, cscallback1, csadurl, cslottery, csluckymoney, cscallback2, cs
from service.game import plane
#import wsgiserver as server
#import gevent.monkey
#gevent.monkey.patch_all()
import server

try:
    import __pypy__
except ImportError:
    __pypy__ = None


class Application(server.Application):

    def startup(self):
        """处理各种数据库链接等

        比如:
            self.db = torndb.Connection(
                host=self.config.mysql_host, database=self.config.mysql_database,
                user=self.config.mysql_user, password=self.config.mysql_password)
        """
        self.db = torndb.Connection(**self.config['mysql'])


class MainHandler(JSONBaseHandler):

    def get(self):
        self.write_json({"d": "helloworld"})


if __name__ == '__main__':
    static_path = os.path.join(os.path.dirname(__file__), "static")

    handlers = [
        (r"/", MainHandler),
        # 抽奖相关
        (r"/game/plane", plane.GameHandler),
        (r"/v1/game/scratch", lottery.ScratchCardHandler),
        (r"/v1/game/bigsmall", lottery.BigSmallHandler),
        (r"/v1/game/round", lottery.RoundHandler),
        (r"/v1/luckymoney", luckymoney.LuckyHandler),
        (r"/v1/luckymoney1", luckymoney1.LuckyHandler),
        (r"/v1/activity", luckymoney.ActivityHandler),
        # 兑换相关
        (r"/v1/exchange/new_order", exchange.NewOrderHandler),
        (r"/v1/exchange/my_orders", exchange.MyOrdersHandler),
        (r"/v1/goods/list", exchange.ListGoodsHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': static_path}),
        # 用户相关
        (r"/v1/user/info", user.UserHandler),
        (r"/v1/user/infoios", user.UseriosHandler),
        (r"/v1/user/bind", user.BindHandler),
        (r"/v1/user/bindfb", user.BindfbHandler),
        (r"/v1/user/points", user.PointsHandler),
        (r"/v1/user/points_detail", user.PointsDetailHandler),
        (r"/v1/user/sign", user.SignHandler),
        (r"/v1/user/signinfo", user.SignInfoHandler),
        (r"/v1/beginner", user.NewUserHandler),
        (r"/v1/dailyreward", user.TodayHandler),
        (r"/v1/othersexchange", user.OthExchangeHandler),
        (r"/v1/invite", invite.CheckInviteHandler),
        # 配置相关
        (r"/v1/config/ad", config.AdConfigHandler),
        (r"/v1/config/changelog", config.ChangelogHandler),
        (r"/v1/announce", config.AnnounceHandler),
        (r"/v1/gofreemission", config.MissionHandler),
        (r"/v1/gomission", config.GomissionHandler),
        (r"/v1/gomission/([^/]+)/.+", config.GomissionHandler),
        (r"/v1/popularize", config.PopularizeHandler),
        (r"/v1/loadpage", config.LoadpageHandler),
        # 广告回调
        (r"/callback/([^/]+)/.+", callback.CallbackHandler),
        (r"/callback1/([^/]+)/.+", callback1.CallbackHandler),
        (r"/callback2/([^/]+)/.+", callback2.CallbackHandler),
        (r"/selfurl/([^/]+)/.+", selfurl.UrlbackHandler),
        (r"/v1/feedback", feedback.FeedbackHandler),
        (r"/v1/share", feedback.ShareHandler),
        # 兑吧
        (r"/v1/exchange/duiba_login", exchange.DuibaUrlHandler),
        (r"/v1/duiba/points", duiba.PointsHandler),
        (r"/v1/duiba/consume", duiba.ConsumeHandler),
        (r"/v1/duiba/notify", duiba.NotifyHandler),
        # youmi广告回调
        (r"/v1/selfurl/([^/]+)/.+", selfurl.AdyouMHandler),
        (r"/v1/ad/([^/]+)/.+", adurl.AdyoumiHandler),

        # 卡卡赚接口
        (r"/kakav1/exchange/new_order", kakaexchange.NewOrderHandler),
        (r"/kakav1/exchange/my_orders", kakaexchange.MyOrdersHandler),
        (r"/kakav1/goods/list", kakaexchange.ListGoodsHandler),
        (r"/kakav1/user/info", kakauser.UserHandler),
        (r"/kakav1/user/infoios", kakauser.UseriosHandler),
        (r"/kakav1/user/bindfb", kakauser.BindfbHandler),
        (r"/kakav1/user/points", kakauser.PointsHandler),
        (r"/kakav1/user/points_detail", kakauser.PointsDetailHandler),
        (r"/kakav1/user/sign", kakauser.SignHandler),
        (r"/kakav1/user/signinfo", kakauser.SignInfoHandler),
        (r"/kakav1/invite", kakainvite.CheckInviteHandler),
        (r"/kakav1/config/ad", kakaconfig.AdConfigHandler),
        (r"/kakav1/config/changelog", kakaconfig.ChangelogHandler),
        (r"/kakacallback/([^/]+)/.+", kakacallback.CallbackHandler),
        (r"/kakaselfurl/([^/]+)/.+", kakaselfurl.UrlbackHandler),
        (r"/kakav1/feedback", kakafeedback.FeedbackHandler),
        (r"/kakav1/share", kakafeedback.ShareHandler),
        # 兑吧
        (r"/kakav1/exchange/duiba_login", kakaexchange.DuibaUrlHandler),
        (r"/kakav1/duiba/points", kakaduiba.PointsHandler),
        (r"/kakav1/duiba/consume", kakaduiba.ConsumeHandler),
        (r"/kakav1/duiba/notify", kakaduiba.NotifyHandler),
        # youmi广告回调
        (r"/kakav1/selfurl/([^/]+)/.+", kakaselfurl.AdyouMHandler),
        (r"/kakav1/ad/([^/]+)/.+", kakaadurl.AdyoumiHandler),

        #超商好康接口
        (r"/csv1/game/scratch", cslottery.ScratchCardHandler),
        (r"/csv1/game/bigsmall", cslottery.BigSmallHandler),
        (r"/csv1/game/round", cslottery.RoundHandler),
        (r"/csv1/luckymoney", csluckymoney.LuckyHandler),
        (r"/csv1/activity", csluckymoney.ActivityHandler),
        # 兑换相关
        (r"/csv1/exchange/new_order", csexchange.NewOrderHandler),
        (r"/csv1/exchange/my_orders", csexchange.MyOrdersHandler),
        (r"/csv1/goods/list", csexchange.ListGoodsHandler),
        # 用户相关
        (r"/csv1/user/info", csuser.UserHandler),
        (r"/csv1/user/infoios", csuser.UseriosHandler),
        (r"/csv1/user/bindfb", csuser.BindfbHandler),
        (r"/csv1/user/points", csuser.PointsHandler),
        (r"/csv1/user/points_detail", csuser.PointsDetailHandler),
        (r"/csv1/user/sign", csuser.SignHandler),
        (r"/csv1/user/signinfo", csuser.SignInfoHandler),
        (r"/csv1/beginner", csuser.NewUserHandler),
        (r"/csv1/dailyreward", csuser.TodayHandler),
        (r"/csv1/othersexchange", csuser.OthExchangeHandler),
        (r"/csv1/invite", csinvite.CheckInviteHandler),
        # 配置相关
        (r"/csv1/config/ad", csconfig.AdConfigHandler),
        (r"/csv1/config/changelog", csconfig.ChangelogHandler),
        (r"/csv1/announce", csconfig.AnnounceHandler),
        (r"/csv1/gofreemission", csconfig.MissionHandler),
        (r"/csv1/gomission", csconfig.GomissionHandler),
        (r"/csv1/gomission/([^/]+)/.+", csconfig.GomissionHandler),
        (r"/csv1/popularize", csconfig.PopularizeHandler),
        (r"/csv1/loadpage", csconfig.LoadpageHandler),
        # 广告回调
        (r"/cscallback/([^/]+)/.+", cscallback.CallbackHandler),
        (r"/cscallback1/([^/]+)/.+", cscallback1.CallbackHandler),
        (r"/cscallback2/([^/]+)/.+", cscallback2.CallbackHandler),
        (r"/csselfurl/([^/]+)/.+", csselfurl.UrlbackHandler),
        (r"/csv1/feedback", csfeedback.FeedbackHandler),
        (r"/csv1/share", csfeedback.ShareHandler),
        # 兑吧
        (r"/csv1/exchange/duiba_login", csexchange.DuibaUrlHandler),
        (r"/csv1/duiba/points", csduiba.PointsHandler),
        (r"/csv1/duiba/consume", csduiba.ConsumeHandler),
        (r"/csv1/duiba/notify", csduiba.NotifyHandler),
        # youmi广告回调
        (r"/csv1/selfurl/([^/]+)/.+", csselfurl.AdyouMHandler),
        (r"/csv1/ad/([^/]+)/.+", csadurl.AdyoumiHandler),
        # 超商相关
        (r"/csv1/business/city", cs.CityHandler),
        (r"/csv1/business/shopstype", cs.ShoptypeHandler),
        (r"/csv1/business/shopdetail", cs.ShopDetailHandler),
        (r"/csv1/business/shops", cs.ShoplistHandler),

    ]

    if __pypy__:
        print("Running in PYPY")
    else:
        print("Running in CPython")

    server.mainloop(Application(handlers))


