#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

兑吧处理接口
@author chenjiehua@youmi.net, lisongjian@youmi.net

"""
""" 兑吧查询接口 """
import constants, protocols
import utils

def check_params(params, appKey, appSecret):
    if params['appKey'] != appKey:
        return False, constants.ERR_KEY_NOT_MATCH
    if params['timestamp'] == '':
        return False, constants.ERR_TIME_NOT_NULL
    params['appSecret'] = appSecret
    sign = params.pop('sign')
    check_sign = utils.md5_sign(params)
    if sign != check_sign:
        return False, constants.ERR_INVALID_SIGN

    return True, ''

class PointsHandler(protocols.JSONBaseHandler):
    """ 用户余额查询 """
    @protocols.unpack_arguments(with_scopeid=False)
    def get(self):
        #log_path = self.config['log']['duiba_log']
        #utils.print_log('duiba', log_path, self.request.uri)
        self.appKey = self.config['duiba']['appKey']
        self.appSecret = self.config['duiba']['appSecret']

        self.params = {}
        kv = self.request.arguments
        for k in kv:
            self.params[k] = kv[k][0].decode('utf-8')

        success, msg = check_params(self.params, self.appKey, self.appSecret)
        if not success:
            self.write_json({"status": "fail", "errorMessage": msg[1]})
            return

        user_info = self.db.get(
                    "SELECT * FROM `user` WHERE `uid` = %s",
                    self.params['uid'])
        self.write_json({"status": "ok", "message": "查询成功", \
                         "data":{"credits": user_info['points']}})


class ConsumeHandler(protocols.JSONBaseHandler):
    """ 积分消耗 """
    @protocols.unpack_arguments(with_scopeid=False)
    def get(self):
        log_path = self.config['log']['duiba_log']
        utils.print_log('duiba', log_path, self.request.uri)
        self.appKey = self.config['duiba']['appKey']
        self.appSecret = self.config['duiba']['appSecret']

        self.params = {}
        kv = self.request.arguments
        # print kv
        for k in kv:
            self.params[k] = kv[k][0].decode('utf-8')

        # 兑换地址
        self.address = ''
        #for add in ['alipay', 'phone', 'qq']:
        #    if self.params[add]:
        #        if add == 'alipay':
        #            self.params[add] = self.params[add].split(':')[0]
        #        self.address = self.params[add]
        self.address = self.params['params']
        self.user_info = self.db.get(
                    "SELECT * FROM `user` WHERE `uid` = %s",
                    self.params['uid'])
        success, msg = check_params(self.params, self.appKey, self.appSecret)
        success, msg = self.__check_valid()
        if not success:
            self.write_json({"status": "fail", "message": "", "errorMessage": msg[1]})
            # print msg[1]
            return
        # 全局订单
        # 增加兑换流水，注意这里是消耗积分，所以是负数
        oid = self.db.execute_lastrowid(
            "INSERT INTO `global_orders` (uid, points, last, type, note)"
            "VALUES (%s, %s, %s, %s, %s)",
            self.params['uid'], -int(self.params['credits']), self.user_info['points'], 5, "兑吧兑换"+self.params['type'])
        description = ''.join(self.params['description'].split(' ')[1:])
        self.params['facePrice'] = int(self.params['facePrice']) / 100.0
        self.params['actualPrice'] = int(self.params['actualPrice']) / 100.0
        p = {
            'uid': self.user_info['uid'],
            'oid': oid,
            'points': self.params['credits'],
            'total_points': self.params['credits'],
            'price': self.params['facePrice'],
            'total_price': self.params['actualPrice'],
            'goods_id': 0,
            'goods_title': description,
            'count': 1,
            'status': 0,
            'duiba': 1,
            'address': self.address,
            'notes': self.params['description'],
            'orderNum': self.params['orderNum'],
            'type': self.params['type'],
            'waitAudit': self.params['waitAudit']
        }
        if int(p['points'])>=int(3000):
            msg = "兑换大于30元,请到兑吧后台审核"
            utils.pushover(self,p['uid'], p['goods_title'], msg)
            # print ">=3000"
        else:
            # print "<3000"
            pass

        self.new_exchange_order(p)
        # 更新用户余额
        remain_points = self.user_info['points'] - long(p['total_points'])
        exchange_points = self.user_info['ex_points'] + long(p['total_points'])
        self.db.execute(
            "UPDATE `user` SET `points` = %s, `ex_points` = %s WHERE `uid` = %s",
            remain_points, exchange_points, p['uid'])

        self.write_json({"status": "ok", "message": "扣除成功", \
                         "data":{"bizId": str(oid)}})


    def new_exchange_order(self, p):
        return self.db.execute(
            "INSERT INTO `exchange_orders` (`uid`, `oid`, `points`, "
            "`total_points`, `price`, `total_price`, `goods_id`, `goods_title`, `count`, "
            "`status`, `duiba`, `address`, `notes`, `orderNum`) "
            "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            p['uid'], p['oid'], p['points'], p['total_points'],
            p['price'], p['total_price'], p['goods_id'], p['goods_title'], p['count'],
            p['status'],p['duiba'], p['address'], "兑吧兑换"+p['type'], p['orderNum'])

    def __check_valid(self):
        # 检查用户状态
        success, msg = True, None
        # 检查用户积分
        if self.user_info['points'] < int(self.params['credits']):
            success, msg = False, constants.ERR_NOT_ENOUGH_POINTS

        return success, msg


class NotifyHandler(protocols.JSONBaseHandler):
    """ 兑换结果通知 """
    def get(self):
        log_path = self.config['log']['duiba_log']
        utils.print_log('duiba', log_path, self.request.uri)
        self.appKey = self.config['duiba']['appKey']
        self.appSecret = self.config['duiba']['appSecret']

        self.params = {}
        kv = self.request.arguments
        # print 'kv'
        # print kv
        for k in kv:
            self.params[k] = kv[k][0].decode('utf-8')

        success, msg = check_params(self.params, self.appKey, self.appSecret)
        if not success:
            self.write_json({"status": "false", "errorMessage": msg[1]})
            return

        print self.params
        order = self.db.get(
                "SELECT * FROM `exchange_orders` WHERE `orderNum`= %s ORDER BY `id` DESC LIMIT 1 ", self.params['orderNum'])
        # 订单不存在
        if not order:
            #self.write_json({"status": "true"})
            self.write('ok')
            return
        self.user_info = self.db.get(
            "SELECT * FROM `user` WHERE `uid` = %s",
            order['uid'])
        # print self.params['orderNum']+'\norderNum'
        if order['orderNum']==self.params['orderNum'] and order['status']!=0:
            self.write('ok')
            return
        # 标记为拒绝的订单无需修改状态
        #if order['status'] in [2, 3]:
        #    self.write_json({"status": "true"})
        #    return

        if self.params['success'].lower() == 'false':
            self.set_order_status(self.params['orderNum'],
                3, self.params['errorMessage'])
            # 兑换失败，退回积分，增加流水
            #FailCheat = self.db.get(
            #    "SELECT count(*) FROM `global_orders` WHERE `uid` = %s AND `type` = '7' AND DATE(`record_time`)=CURDATE()",
            #    order['uid'])
            #print FailCheat['count(*)']
            #if FailCheat['count(*)']<3:
            self.db.execute(
                "UPDATE  `user` SET  `points` = `points` + %s,\
                `ex_points` = `ex_points` - %s "
                "WHERE `user`.`uid` = %s", order['points'], order['points'], order['uid'])
            self.new_global_order(
                order['uid'], order['points'], self.user_info['points'], 7,
                u"兑换失败，退回 %d 点数" % order['points'])
            msg = "兑吧兑换失败"
            # self.pushover(order['uid'],order['goods_title'],msg)
            #elif FailCheat['count(*)']>=3:
            #    msg = "兑吧兑换失败超过三次，积分不给返还，请注意"
            #    self.pushover(order['uid'], order['goods_title'], msg)
        elif self.params['success'].lower() == 'true':
            notes = self.params['errorMessage'] if self.params['errorMessage'] else order['notes']
            self.set_order_status(self.params['orderNum'], 1, notes)
            self.push(self.user_info['scopeid'],order['goods_title'])
        else:
            #self.write_json({"status": "false", "errorMessage": "code error"})
            self.write('ok')
            return

        #self.write_json({"status": "true"})
        self.write('ok')

    def new_global_order(self, uid, points, last, typ, note):
        return self.db.execute(
            "INSERT INTO `global_orders` (`uid`, `points`, `last`, `type`, `note`)"
            "VALUES (%s, %s, %s, %s, %s)", uid, points, last, typ, note)

    def set_order_status(self, orderNum, status, notes):
        return self.db.execute(
            "UPDATE `exchange_orders` SET `status` = %s, `notes` = %s "
            "WHERE `orderNum` = %s", status, notes, orderNum)


    def push(self,scopeid,title):
        """推送到Parse"""
        import httplib,json
        connection = httplib.HTTPSConnection('api.parse.com', 443)
        connection.connect()
        connection.request('POST', '/1/push', json.dumps({
            "where": {
                 "scopeid": ""+scopeid+""
            },
            "data": {
                 "action": 1,
                 "alert": "恭喜，"+title.encode("utf-8")+"兌換成功了。點擊查看"
            }
            }), {
            "X-Parse-Application-Id": self.config['push']['ApplicationId'],
            "X-Parse-REST-API-Key": self.config['push']['APIKey'],
            "Content-Type": "application/json"
             })

    def pushover(self,uid,title,msg):
        """Pushover"""
        import urllib,httplib
        conn = httplib.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
            urllib.urlencode({
                "token": self.config['pushover']['token'],
                "user": self.config['pushover']['user'],
                "message": "uid"+str(uid)+msg,
            }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()
