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
import time


class NewOrderHandler(protocols.JSONBaseHandler):
    """ 兑换商品 """

    @protocols.unpack_arguments()
    def post(self):
        goods_id = self.arguments.get("goods_id")
        count = int(self.arguments.get("count"))
        address = self.arguments.get("address")

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
            self.current_user['id'])

        if total_points > user_info['points']:
            self.return_error(constants.ERR_NOT_ENOUGH_POINTS, "余额不足")
            return

        # 创建订单流水
        # 增加兑换流水，注意这里是消耗积分，所以是负数
        oid = self.db.execute_lastrowid(
            "INSERT INTO `global_orders` (uid, points, last)"
            "VALUES (%s, %s, %s)",
            self.current_user['id'], -total_points, user_info['points'])

        # 创建货物订单
        self.db.execute(
            "INSERT INTO `exchange_orders` (uid, oid, points, total_points, "
            "price, total_price, goods_id, goods_title, count, address) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            self.current_user['id'], oid, goods_info['points'], total_points,
            goods_info['price'], goods_info['price'] * count,
            goods_id, goods_info['title'], count, address)

        # 更新用户余额
        remain_points = user_info['points'] - total_points
        exchange_points = user_info['ex_points'] + total_points
        self.db.execute(
            "UPDATE `user` SET `points` = %s, `ex_points` = %s WHERE `uid` = %s",
            remain_points, exchange_points, self.current_user['id'])

        # 增加货物兑换次数标记
        self.db.execute(
            "UPDATE `exchange_goods` SET `exchange_counts` = `exchange_counts` + 1"
            " WHERE `goods_id` = %s",
            goods_id)

        self.return_success()


class ListGoodsHandler(protocols.JSONBaseHandler):
    """ 获取可兑换货物列表 """

    @protocols.unpack_arguments()
    def get(self):
        types = self.db.query("SELECT * FROM `exchange_types`")

        formated_goods_list = []
        for typ in types:
            formated_goods_list.append({
                "title": typ['title'],
                "address_type": typ['address_type'],
                'icon': self.config['goods']['static_url'] + typ['icon'],
                "list": self.get_goods(typ['id']),
            })

        self.return_result({"goods": formated_goods_list})

    def get_goods(self, type_id):
        goods = self.db.query(
            "SELECT * FROM `exchange_goods` WHERE `type_id` = %s", type_id)
        formated_goods_list = []
        for item in goods:
            formated_item = {
                'gid': item['goods_id'],
                'title': item['title'],
                'desc': item['description'],
                'price': item['points'],  # 客户端的单价是服务器端记录的商品积分价值
                'exchange_counts': item['exchange_counts'],
            }
            formated_goods_list.append(formated_item)
        return formated_goods_list


class MyOrdersHandler(protocols.JSONBaseHandler):
    """ 获取订单列表 """

    order_status = {
        0: "待审核",
        1: "审核通过"
    }

    @protocols.unpack_arguments()
    def get(self):
        orders = self.db.query(
            "SELECT * FROM `exchange_orders` WHERE `uid` = %s",
            self.current_user['id'])

        if not orders:
            self.return_result({"orders": []})
            return

        formated_orders_list = []
        for item in orders:
            formated_item = {
                'oid': item['id'],
                'status': self.order_status[item['status']],
                'title': item['goods_title'],
                'notes': item['notes'],
                'create_time': time.mktime(item['create_time'].timetuple()),
            }
            formated_orders_list.append(formated_item)

        self.return_result({"orders": formated_orders_list})


class LatestOrdersHandler(protocols.JSONBaseHandler):
    """" 最新兑换记录50条 """

    @protocols.unpack_arguments()
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
                'title': item['goods_title'],
                'count': item['count'],
                'create_time': time.mktime(item['create_time'].timetuple()),
            }
            formated_orders_list.append(formated_item)

        self.return_result({"orders": formated_orders_list})
