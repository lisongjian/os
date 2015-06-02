#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

超商模块

@author lisongjian

"""

import protocols
#import tornado.web
#import tornado.escape
#import constants
#import time,datetime
#import json,httplib


class CityHandler(protocols.JSONBaseHandler):
    """城市列表"""

    @protocols.unpack_csarguments_byscopeid(with_scopeid=False)
    def get(self):
        #platform = self.arguments.get('platform')
        all_city = self.db.query(
            "SELECT * FROM `cs_city` WHERE `status`=1 ORDER BY 'id' DESC ")
        Acitys = []
        for city in all_city:
            Acitys.append({
                "id": city['id'],
                "name": city['name'],
                })

        self.return_result({"list":Acitys})


class ShoptypeHandler(protocols.JSONBaseHandler):
    """商铺类别"""

    @protocols.unpack_csarguments_byscopeid(with_scopeid=False)
    def get(self):
        #platform = self.arguments.get('platform')
        all_shop = self.db.query(
            "SELECT * FROM `cs_shop_type` WHERE `status`=1 ORDER BY 'id' DESC ")
        Ashops = []
        for shop in all_shop:
            Ashops.append({
                "id": shop['id'],
                "name": shop['name'],
                })

        self.return_result({"list":Ashops})


class ShoplistHandler(protocols.JSONBaseHandler):
    """商铺列表"""

    @protocols.unpack_csarguments_byscopeid(with_scopeid=False)
    def get(self):
        #platform = self.arguments.get('platform')
        cityid = int(self.arguments.get('cityid', 1))
        shopstypeid = int(self.arguments.get('shopstypeid', 1))
        print `cityid` + `shopstypeid`
        if shopstypeid !=0:
            all_shops = self.db.query(
                "SELECT * FROM `cs_shops` WHERE `cityid`=%s AND `shopstypeid`=%s \
                ORDER BY 'id' DESC ", cityid, shopstypeid)
        else:
            all_shops = self.db.query(
                "SELECT * FROM `cs_shops` WHERE `cityid`=%s ORDER BY 'id' DESC ", cityid)

        Ashops = []
        for shop in all_shops:
            Ashops.append({
                "id": shop['id'],
                "name": shop['name'],
                "city": shop['city'],
                "district": shop['district'],
                "street": shop['street'],
                "phone": shop['phone'],
                "lot": shop['lot'],
                "lat": shop['lat'],
                "shopstypeid": shopstypeid,
                "cityid": cityid,
                })

        self.return_result({"lists":Ashops})


class ShopDetailHandler(protocols.JSONBaseHandler):
    """详情列表"""

    @protocols.unpack_csarguments_byscopeid(with_scopeid=False)
    def get(self):
        #platform = self.arguments.get('platform')
        cityid = int(self.arguments.get('cityid', 1))
        shopstypeid = int(self.arguments.get('shopstypeid', 1))
        # print `cityid` + `shopstypeid`
        if shopstypeid !=0:
            all_shops = self.db.get(
                "SELECT * FROM `cs_shops` WHERE `cityid`=%s AND `shopstypeid`=%s \
                ORDER BY 'id' LIMIT 1 ", cityid, shopstypeid)
        else:
            all_shops = self.db.get(
                "SELECT * FROM `cs_shops` WHERE `cityid`=%s ORDER BY 'id' LIMIT 1 ", cityid)

        Acards = []
        all_cards=self.db.query(
            "SELECT * FROM `exchange_goods` WHERE `type_id`=%s ORDER BY 'id' DESC ", all_shops['type_id'])
        for card in all_cards:
            icon_url=self.db.get(
                "SELECT `icon`,`id` from `exchange_types` WHERE `id`=%s", card['type_id'])
            Acards.append({
                "cid": card['goods_id'],
                "cname": card['title'],
                "cprice": card['price'],
                "cpoints": card['points'],
                "step": card['use'],
                "remark": card['note'],
                "iconurl": "http://api.gofree.cc/static/" + icon_url['icon'],
                })

        self.return_result({"cards":Acards})



