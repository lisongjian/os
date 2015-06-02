#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author cairuitao@gmail.com
#
""" 常量定义 """

""" Tornado Server 定义 """

# 接收到关闭信号后多少秒后才真正重启
MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 1
# Listen IPV4 only
IPV4_ONLY = True

""" 协议、校验错误 """

ERR_PROTOCOL_ERROR = (-1001, "协议解析错误")
ERR_INTERNAL_ERROR = (-1002, "内部错误")
ERR_DECRYPT_FAIL = (-1003, "解密失败")
ERR_INVALID_USER = (-1004, "非法用户")
ERR_INVALID_TOKEN = (-1005, "非法token")
ERR_INVALID_SCOPEID = (-1006, "非法SCOPEID")
ERR_INVALID_FACEBOOK = (-1007, "非法FACEBOOK帐号")

""" 兑换相关错误信息 """

ERR_INVALID_GOODS_COUNT = (-4001, "兑换商品数量错误")
ERR_NOT_ENOUGH_POINTS = (-4002, "余额不足")
ERR_INVALID_GOODS_ID = (-4003, "错误的商品编号")

""" 签到、等级奖励 """

ERR_REPEAT_SIGN = (-5001, "当天重复签到")
ERR_REPEAT_AWARD = (-5002, "该等级奖励已领取")
ERR_NOT_ENOUGH_GRADE = (-5003, "等级不够")
ERR_NOT_NEW_USER = (-5004, "新用户奖励已领取")

""" 邀请、分享"""

ERR_NOT_INVITE = (-6001, "没有此邀请码")
ERR_NOT_SELF = (-6002, "不能邀请自己")
ERR_HAD_SHARE = (-6003, "已分享过应用")
ERR_NOT_NULL = (-6004, "邀请码已填过")

""" 兑吧相关错误信息 """

ERR_KEY_NOT_MATCH = (-7001, "兑吧KEY错误")
ERR_TIME_NOT_NULL = (-7002, "时间不能为空")
ERR_INVALID_SIGN = (-7003, "签名错误")
