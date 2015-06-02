#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author cairuitao@gmail.com
#
""" 各种优惠券获取api """

import protocols
import tornado.web
import datetime


def fill_zero(number):
    """ 对于小于10的自动补上前面的0 """
    return "0%s" % number if number < 10 else number


def format_timedelta(timedelta_value):
    """ 将timedelta格式化为 %H:%m:%s """

    hours, remainder = divmod(timedelta_value.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '%s:%s:%s' % (hours, fill_zero(minutes), fill_zero(seconds))


class MetaHandler(protocols.JSONBaseHandler):
    """ 优惠券元数据 """

    @protocols.unpack_arguments()
    def get(self):
        meta = self.db.query("SELECT * FROM `coupon_brands`")
        formated_meta = []
        for brand in meta:
            formated_brand = {
                'id': brand['id'],
                'name': brand['name'],
                'img': self.config['coupons']['static_url'] + brand['img'],
            }
            formated_meta.append(formated_brand)

        self.return_result({"meta": formated_meta})


class ListCouponsHandler(protocols.JSONBaseHandler):
    """ 获取优惠券 """

    @protocols.unpack_arguments(with_token=False)
    @tornado.web.asynchronous
    def get(self):
        skip = int(self.arguments.get("skip", 0))  # 跳过前多少
        limit = int(self.arguments.get("limit", 5))  # 获取多少优惠券
        brand_id = int(self.arguments.get("brand_id", 0))  # 获取什么类型的优惠券

        # TODO Cache here
        now = datetime.date.today()

        if brand_id > 0:
            coupons = self.db.query(
                "SELECT `coupons`.`id`, `coupons`.`img`, `coupons`.`title`, `coupons`.`end_date`, "
                "`coupons`.`display_times`, `coupon_brands`.`name` as `brand_name` "
                "FROM `coupons` LEFT JOIN `coupon_brands` ON "
                "`brand_id` = `coupon_brands`.`id` "
                "WHERE `brand_id` = %s AND `end_date` >= %s LIMIT %s,%s",
                brand_id, now, skip, limit)
        else:
            coupons = self.db.query(
                "SELECT `coupons`.`id`, `coupons`.`img`, `coupons`.`title`, `coupons`.`end_date`, "
                "`coupons`.`display_times`, `coupon_brands`.`name` as `brand_name` "
                "FROM `coupons` LEFT JOIN `coupon_brands` ON "
                "`brand_id` = `coupon_brands`.`id` "
                "WHERE `end_date` >= %s LIMIT %s,%s",
                now, skip, limit)

        formated_coupons_list = []
        coupons_id = []
        for coupon in coupons:
            formated_coupon = {
                'title': coupon['title'],
                'brand': coupon['brand_name'],
                'end_date': "有效期至%s" % (coupon['end_date'].strftime("%Y年%m月%d日")),
                'img': self.config['coupons']['static_url'] + coupon['img'],
                'display_times': coupon['display_times'] + 1,
            }
            formated_coupons_list.append(formated_coupon)
            coupons_id.append(coupon['id'])

        self.return_result({
            "skip": skip,
            "limit": limit,
            "coupons": formated_coupons_list})

        # 更新展示次数
        # FIXME 这样弄效率会有问题
        if len(formated_coupons_list) > 0:
            sql = "UPDATE `coupons` SET `display_times` = `display_times` + 1 WHERE `id` IN (%s)"
            in_p = ', '.join(list(map(lambda x: '%s', coupons_id)))
            sql = sql % in_p
            self.db.execute(sql, *coupons_id)
        return
