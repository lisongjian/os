#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

广告平台回调处理
@author zhenyong, lisongjian@youmi.net

"""

from protocols import JSONBaseHandler
#import datetime
#import time as mtime
import logging
import logging.config
import hashlib
import json,httplib
import datetime
import csv
import utils

class CallbackHandler(JSONBaseHandler):
    logger = None  # logger handler

    def get(self, platform):
        """接收广告平台回调"""
        if platform == 'tapjoyaos' :
            self.__save_tapjoy_aos_order()
            self.write('ok')
            self.__log(self.ip)
        elif platform == 'offerboard':
            self.__save_offerboard_aos_order()
            self.write('1')
            self.__log(self.ip)
        elif platform == 'native':
            self.__save_nativex_order()
            self.write('ok')
            self.__log(self.ip)
        elif platform == 'super':
            self.__save_super_order()
            self.write('ok')
            self.__log(self.ip)
        elif platform == 'trialpay':
            self.__save_trialpay_order()
            self.write('1')
            self.__log(self.ip)
        elif platform == 'supersonicads':
            self.__save_supersonicads_order()
            self.write(self.eventId+':OK')
            self.__log(self.ip)
        elif platform == 'youmi':
            self.__save_youmi_order()
            self.write('ok')
            self.__log(self.ip)
        elif platform == 'vungle':
            self.__save_vungle_order()
            self.write('ok')
            self.__log(self.ip)
        elif platform == 'aarki':
            self.__save_aarki_order()
            self.write('ok')
            self.__log(self.ip)
        elif platform == 'fyber':
            self.__save_fyber_order()
            self.write('ok')
            self.__log(self.ip)
        elif platform == 'appdriver':
            self.__save_appdriver_order()
            self.write('ok')
            self.__log(self.ip)
        elif platform == 'flurry':
            self.__save_flurry_order()
            self.write('ok')
            self.__log(self.ip)
        elif platform == 'appdriveros':
            self.__save_appdriveros_order()
            self.__log(self.ip)
        elif platform == 'adcolony':
            self.__save_adcolony_order()
            self.__log(self.ip)
        elif platform == 'tokenads':
            self.__save_tokenads_order()
            self.__log(self.ip)
            self.write('ok')
        elif platform == 'duomeng':
            self.__save_duomeng_order()
            self.write('ok')
            self.__log(self.ip)
        elif platform == 'tvn':
            self.__save_tvn_order()
            self.write('ok')
            self.__log(self.ip)
        elif platform == 'adxmi':
            self.__save_adxmi_order()
            self.write('ok')
            self.__log(self.ip)

        # IOS回调接口
        elif platform == 'youmiios':
            self.__save_youmiios_order()
            self.write('ok')
            self.__log(self.ip)
        elif platform == 'supersonicadsios':
            self.__save_supersonicadsios_order()
            self.write(self.eventId+':OK')
            self.__log(self.ip)
        elif platform == 'aarkiios':
            self.__save_aarkiios_order()
            self.write('ok')
            self.__log(self.ip)
        elif platform == 'tapjoyios':
            self.__save_tapjoy_ios_order()
            self.write('ok')
            self.__log(self.ip)
        elif platform == 'appdriverios':
            self.__save_appdriver_ios_order()
            self.write('ok')
            self.__log(self.ip)
        elif platform == 'nativexios':
            self.__save_nativexios_order()
            self.write('ok')
            self.__log(self.ip)
        elif platform == 'metapsios':
            self.__save_metapsios_order()
            self.write('ok')
            self.__log(self.ip)
        elif platform == 'fyberios':
            self.__save_fyberios_order()
            self.write('ok')
            self.__log(self.ip)
        elif platform == 'trialpayios':
            self.__save_trialpayios_order()
            self.write('ok')
            self.__log(self.ip)
        elif platform == 'vungleios':
            self.__save_vungleios_order()
            self.write('ok')
            self.__log(self.ip)
        elif platform == 'appdriverosios':
            self.__save_appdriverosios_order()
            self.__log(self.ip)
        elif platform == 'adcolonyios':
            self.__save_adcolonyios_order()
            self.__log(self.ip)
        elif platform == 'tokenadsios':
            self.__save_tokenadsios_order()
            self.__log(self.ip)
            self.write('ok')
        elif platform == 'iostvn':
            self.__save_iostvn_order()
            self.write('ok')
            self.__log(self.ip)
        elif platform == 'iosduomeng':
            self.__save_iosduomeng_order()
            self.write('ok')
            self.__log(self.ip)
        #elif platform == 'superRepeat':
        #    self.getSupersonicRepeat()
        elif platform == 'adxmiios':
            self.__save_adxmi_order()
            self.write('ok')
            self.__log(self.ip)

        elif platform == 'buchang':
            pass
            #self.getPaypoint()
        #ip = ""
        #self.__log(ip)


    #tapjoy广告平台回调
    def __save_tapjoy_aos_order(self):
        """Tapjoy aos订单"""
        #info = json.loads(self.request.body)
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1 LIMIT 1", self.ip)
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            return
        params = {}
        params['scopeid'] = self.get_argument('snuid', '')
        #params['token'] = self.get_argument('snuid', None)
        params['app_id'] = self.get_argument('app_id', None)
        params['publisher_user_id'] = self.get_argument('publisher_user_id', None)
        params['currency_id'] = self.get_argument('currency_id', None)
        params['library_version'] = self.get_argument('library_version', None)
        params['device_ip'] = self.get_argument('device_ip', None)
        params['timestamp'] = self.get_argument('timestamp', None)
        params['verifier'] = self.get_argument('verifier', None)
        params['max'] = self.get_argument('max', None)
        params['device_type'] = self.get_argument('device_type', None)
        params['order'] = "Tapjoy紅利"
        params['ad'] = "Tapjoy紅利"
        params['getPoint'] = self.get_argument('currency', None)
        params['mac_address'] = self.get_argument('mac_address', None)
        detail = 'aos'
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s AND `appType`=0",
            params['scopeid'])
        if not uid:
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['scopeid'])
            return
        self.saveOrder(
            uid['uid'], params['order'], params['order'], 0, params['scopeid'], 0,
            params['getPoint'], 0, 0, 0, 0, 100, 3, detail)
        self.push(params['scopeid'],params['ad'],params['getPoint'])
        self.pushEng(params['scopeid'],params['ad'],params['getPoint'])
        self.pushIosAppstore(params['scopeid'],params['ad'],params['getPoint'])

        #secret_key = MD5 hash 值
        #简单防欺诈
        valild = [
        #    idkey,
        #    uid,
        #    points,
           #secret_key,
        ]
        valild_str = ':'.join(str(valild))
        return hashlib.md5(valild_str).hexdigest()

    #metaps广告平台回调
    def __save_offerboard_aos_order(self):
        params={}
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1 LIMIT 1", self.ip)
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            return
        params['scopeid'] = self.get_argument('cuid', None)#用户的scopeid字符串
        #params['token'] = self.get_argument('cuid', None)#用户的token字符串
        params['getPoint'] =self.get_argument('ucur', None)#用户报酬
        params['point'] = self.get_argument('point', None)#媒体应用获得的point数量
        params['grid'] = self.get_argument('grid', None)#通过 Offerboard 获得成果的唯一ID
        params['order'] = "Metaps紅利"
        params['ad'] = "Metaps紅利"
        params['scn'] = self.get_argument('scn', None)#初始化显示积分墙方法时设定的 scenario 字符串
        params['adid'] = self.get_argument('aid', None)#广告应用的 ID
        detail = 'aos'
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s AND `appType`=0",
            params['scopeid'])
        if not uid:
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['scopeid'])
            return
        self.saveOrder(
            uid['uid'], params['order'], params['order'], params['adid'], params['scopeid'], 0,
            params['getPoint'], 0, 0, 0, 0, 101, 3, detail)
        self.push(params['scopeid'],params['ad'],params['getPoint'])
        self.pushEng(params['scopeid'],params['ad'],params['getPoint'])
        self.pushIosAppstore(params['scopeid'],params['ad'],params['getPoint'])

    def __save_super_order(self):
        pass
    def __save_aarkiios_order(self):
        params = {}
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1 LIMIT 1", self.ip)
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            return
        params['scopeid'] = self.get_argument('user', None)
        params['order'] = "aarki紅利"
        params['adid'] = self.get_argument('id', None)
        params['ph'] = self.get_argument('ph', None)
        params['device'] = self.get_argument('dev', None)
        params['dollars'] = self.get_argument('dollars', None)
        params['pid'] = self.get_argument('pid', None)
        params['ad'] = "aarki紅利"
        params['getPoint'] = self.get_argument('units', "")
        detail= 'ios'
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s AND `appType`=0",
            params['scopeid'])
        if not uid:
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['scopeid'])
            return
        self.saveOrder(
            uid['uid'], params['order'], params['ad'], params['adid'], params['scopeid'], 0,
            params['getPoint'], params['dollars'], 0, params['device'], 0, 103, 5, detail)
        self.push(params['scopeid'],params['ad'],params['getPoint'])
        self.pushEng(params['scopeid'],params['ad'],params['getPoint'])
        self.pushIosAppstore(params['scopeid'],params['ad'],params['getPoint'])

    def __save_supersonicadsios_order(self):
        params = {}
        params['scopeid'] = self.get_argument('appUserId', None)
        params['timestamp'] = self.get_argument('timestamp', None)
        params['publisherSubId'] = self.get_argument('publisherSubId', None)
        params['country'] = self.get_argument('country', None)
        params['order'] = "Supersonicads紅利"
        params['ad'] = "Supersonicads紅利"
        params['getPoint'] = self.get_argument('rewards', None)
        params['adid'] = self.get_argument('eventId', None)
        params['sig'] = self.get_argument('signature', None)
        params['key'] = '8231fb'
        detail = 'ios'
        self.eventId = params['adid']
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s AND `appType`=0",
            params['scopeid'])
        if not uid:
            return
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1 LIMIT 1", self.ip)
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user and ip_info:
            self.ip = "&ERRip="+str(self.ip) +"&BlackUser="+str(params['scopeid'])
            return
        elif black_user:
            self.ip = "&BlackUser="+str(params['scopeid'])
            return
        elif ip_info:
            self.ip = "&ERRip="+str(self.ip)
            return
        elif self.ip == '79.125.5.179' or self.ip =='79.125.26.193' or self.ip == '79.125.117.130' \
                or self.ip == '176.34.224.39' or self.ip == '176.34.224.41' or self.ip == '176.34.224.49' or self.ip == '172.16.5.144':
            pass
        else:
            if black_user and ip_info:
                self.ip = "&ERRip="+str(self.ip) +"&BlackUser="+str(params['scopeid'])
                return
            self.ip = "&ERRip="+str(self.ip)
            return
        self.info = self.db.get(
                "SELECT * FROM `callback_order` WHERE `user`=%s AND `adid`=%s AND `ad_source`=104",
                uid['uid'], params['adid'])
        samePoint = self.db.get(
                "SELECT * FROM `callback_order` WHERE `user`=%s AND `ad_source`=104 \
                AND `points`>299 ORDER BY `time` DESC LIMIT 1", uid['uid'])
        if samePoint:
            diff = datetime.datetime.now()-samePoint['time']-datetime.timedelta(hours=8)
            if str(samePoint['points'])==params['getPoint'] and diff<=datetime.timedelta(seconds=600):
                return
        #secret_key = MD5 hash 值
        #简单防欺诈
        valild =  params['timestamp'] + params['adid'] + params['scopeid'] + params['getPoint'] + params['key']
        self.valild_str =  hashlib.md5(valild).hexdigest()
        self.sig = params['sig']
        if (not self.info) and (self.valild_str==self.sig):
            self.saveOrder(
                uid['uid'], params['order'], params['order'], params['adid'], params['scopeid'], 0,
                params['getPoint'], 0, 0, 0, params['sig'], 104, 5, detail)
            self.push(params['scopeid'],params['ad'],params['getPoint'])
            self.pushEng(params['scopeid'],params['ad'],params['getPoint'])
            self.pushIosAppstore(params['scopeid'],params['ad'],params['getPoint'])
        else:
            #print "Already processed!"
            pass
    def __save_nativexios_order(self):
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        pass
    def __save_vungleios_order(self):
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        pass
    def __save_trialpayios_order(self):
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        pass
    def __save_metapsios_order(self):
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        pass
    def __save_tapjoy_ios_order(self):
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        pass
    def __save_tokenadsios_order(self):
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        pass
    def __save_tvn_order(self):
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        pass
    def __save_iostvn_order(self):
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        pass

    def __save_appdriverosios_order(self):
        params = {}
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        if self.ip == '54.251.141.1' or self.ip =='54.251.161.122':
            pass
        else:
            self.ip = "&ERRip="+str(self.ip)
            self.write('0')
            return
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1 LIMIT 1", self.ip)
        params['ad'] = "appdriver紅利"
        params['getPoint'] = self.get_argument('point', "")
        params['scopeid'] = self.get_argument('identifier', '')
        params['timestamp'] = self.get_argument('accepted_time', '')
        params['server_ip'] = self.get_argument('Userip', '')
        params['adid'] = self.get_argument('achieve_id', '')
        params['advertisement_name']=self.get_argument('advertisement_name', '')
        params['order'] = self.get_argument('campaign_name', '')
        params['advertisement_id'] = self.get_argument('advertisement_id','')
        detail = " ios ( 应用名:"+params['order']+" |获取方式:"+params['advertisement_name']+ \
                " |任务唯一id:"+params['adid']+" |媒体id:"+params['advertisement_id']+" )"
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            self.write('0')
            return
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s AND `appType`=0",
            params['scopeid'])
        if not uid:
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['scopeid'])
            return
        info = self.db.get(
            "SELECT * FROM `callback_order` WHERE `user`=%s and `order`=%s \
            and `adid`= %s and `ad_source`=110 LIMIT 1",
            uid['uid'], params['order'], params['adid'])
        if not info:
            self.saveOrder(
                uid['uid'], params['order'], params['ad'], params['adid'], params['scopeid'], 0,
                params['getPoint'], 0, params['timestamp'], 0, 0, 110, 3, detail)
            self.push(params['scopeid'],params['ad'],params['getPoint'])
            self.pushEng(params['scopeid'],params['ad'],params['getPoint'])
            self.pushIosAppstore(params['scopeid'],params['ad'],params['getPoint'])
            self.write('1')
        else:
            self.write('0')

    def __save_adcolonyios_order(self):
        params = {}
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1 LIMIT 1", self.ip)
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            return
        params['scopeid'] = self.get_argument('custom_id', '')
        params['ad'] = "adcolony紅利"
        params['order'] = "adcolony紅利"
        params['getPoint'] = int(float(self.get_argument('amount', "")))
        params['trans_id'] = self.get_argument('id', '')
        params['dev_id'] = self.get_argument('uid', '')
        params['currency'] = self.get_argument('currency', '')
        params['verifier'] = self.get_argument('verifier', '')
        params['key'] = "v4vc14ba415454424854a9"
        detail = 'ios'
        #secret_key = MD5 hash 值
        #简单防欺诈
        valild =  "" + params['trans_id'] + params['dev_id'] + str(params['getPoint']) + params['currency'] + params['key'] +params['scopeid']
        # print valild
        self.valild_str =  hashlib.md5(valild).hexdigest()
        # print self.valild_str+"  valild_str"
        # print params['verifier']+" GetVerifier"
        if self.valild_str!=params['verifier']:
            self.write('vc_decline')
            return
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s AND `appType`=0",
            params['scopeid'])
        if uid==None:
            self.write('vc_decline')
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['scopeid'])
            return
        cheat = self.db.get(
            "SELECT points, count(*) FROM `callback_order` WHERE `user` = %s  AND `ad_source` = '113' AND DATE(`time`)=CURDATE() ",
            uid['uid'])
        if cheat:
            if cheat['count(*)'] < 10:
                self.saveOrder(
                    uid['uid'], params['order'], params['ad'], params['trans_id'], params['scopeid'], 0,
                    params['getPoint'], 0, 0, params['dev_id'], 0, 113, 5, detail)
                self.push(params['scopeid'],params['ad'],params['getPoint'])
                self.pushEng(params['scopeid'],params['ad'],params['getPoint'])
                self.pushIosAppstore(params['scopeid'],params['ad'],params['getPoint'])
                self.write('vc_success')
                return
            else:
            #    self.pushoverWarn(uid['uid'])
                self.write('vc_decline')
                return


    def __getPayPointlist(self):
        self.getSign()
        self.render('test.html', datas=self.datas)
        #self.write("<td>user"+str(self.user)+"</td>")

    def __getSupersonicRepeatlist(self):
        self.getSupersonicRepeat()
        self.render('test.html', datas=self.datas)
        self.write("<td>user"+str(self.user)+"</td>")

    def __save_supersonicads_order(self):
        params = {}
        params['scopeid'] = self.get_argument('appUserId', None)
        params['timestamp'] = self.get_argument('timestamp', None)
        params['publisherSubId'] = self.get_argument('publisherSubId', None)
        params['country'] = self.get_argument('country', None)
        params['order'] = "Supersonicads紅利"
        params['ad'] = "Supersonicads紅利"
        params['getPoint'] = self.get_argument('rewards', None)
        params['adid'] = self.get_argument('eventId', None)
        params['sig'] = self.get_argument('signature', None)
        params['key'] = '8231fb'
        detail = 'aos'
        self.eventId = params['adid']
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1 LIMIT 1", self.ip)
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            return
        # 服务器ip
        '''
        if self.ip == '79.125.5.179' or self.ip =='79.125.26.193' or self.ip == '79.125.117.130' \
                or self.ip == '176.34.224.39' or self.ip == '176.34.224.41' or self.ip == '176.34.224.49' \
                or self.ip == '58.62.17.190':
            pass
        else:
            self.ip = "&ERRip="+str(self.ip)
            return
        '''
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s AND `appType`=0",
            params['scopeid'])
        if not uid:
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['scopeid'])
            return
        self.info = self.db.get(
                "SELECT * FROM `callback_order` WHERE `user`=%s AND `adid`=%s AND `ad_source`=104",
                uid['uid'], params['adid'])
        samePoint = self.db.get(
                "SELECT * FROM `callback_order` WHERE `user`=%s AND `ad_source`=104 \
                AND `points`>299 ORDER BY `time` DESC LIMIT 1", uid['uid'])
        if samePoint:
            diff = datetime.datetime.now()-samePoint['time']-datetime.timedelta(hours=8)
            #print diff
            #print 'samePoint'
            if str(samePoint['points'])==params['getPoint'] and diff<=datetime.timedelta(seconds=600):
                #print 'err less than 10 min'
                return
        #secret_key = MD5 hash 值
        #简单防欺诈
        valild =  params['timestamp'] + params['adid'] + params['scopeid'] + params['getPoint'] + params['key']
        self.valild_str =  hashlib.md5(valild).hexdigest()
        #print self.valild_str
        #print uid['uid']
        self.sig = params['sig']
        #print self.sig
        #print self.info
        if (not self.info) and (self.valild_str==self.sig):
            self.saveOrder(
                uid['uid'], params['order'], params['order'], params['adid'], params['scopeid'], 0,
                params['getPoint'], 0, 0, 0, params['sig'], 104, 3, detail)
            self.push(params['scopeid'],params['ad'],params['getPoint'])
            self.pushEng(params['scopeid'],params['ad'],params['getPoint'])
            self.pushIosAppstore(params['scopeid'],params['ad'],params['getPoint'])
        else:
            #print "Already processed!"
            pass

    def __save_aarki_order(self):
        params = {}
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1 LIMIT 1", self.ip)
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            return
        params['scopeid'] = self.get_argument('user', None)
        params['order'] = "aarki紅利"
        params['adid'] = self.get_argument('id', None)
        params['ph'] = self.get_argument('ph', None)
        params['device'] = self.get_argument('dev', None)
        params['dollars'] = self.get_argument('dollars', None)
        params['pid'] = self.get_argument('pid', None)
        params['ad'] = "aarki紅利"
        params['getPoint'] = self.get_argument('units', "")
        detail = 'aos'
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s AND `appType`=0",
            params['scopeid'])
        if not uid:
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['scopeid'])
            return
        self.saveOrder(
            uid['uid'], params['order'], params['ad'], params['adid'], params['scopeid'], 0,
            params['getPoint'], params['dollars'], 0, params['device'], 0, 103, 3, detail)
        self.push(params['scopeid'],params['ad'],params['getPoint'])
        self.pushEng(params['scopeid'],params['ad'],params['getPoint'])
        self.pushIosAppstore(params['scopeid'],params['ad'],params['getPoint'])


    def __save_nativex_order(self):
        params = {}
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1 LIMIT 1", self.ip)
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            return
        params['scopeid'] = self.get_argument('uid', None)
        params['order'] = "nativeX紅利"
        params['adid'] = self.get_argument('offerid', None)
        params['ad'] = "nativeX紅利"
        params['getPoint'] = int(float(self.get_argument('currency', "")))
        detail = 'aos'
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s AND `appType`=0",
            params['scopeid'])
        if not uid:
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['scopeid'])
            return
        self.saveOrder(
            uid['uid'], params['order'], params['ad'], params['adid'], params['scopeid'], 0,
            params['getPoint'], 0, 0, 0, 0, 102, 3, detail)
        self.push(params['scopeid'],params['ad'],params['getPoint'])

    def __save_appdriver_order(self):
        params = {}
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1 LIMIT 1", self.ip)
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            return
        params['scopeid'] = self.get_argument('identifier', None)
        params['device'] = self.get_argument('user', None)  # imei
        params['adid'] = self.get_argument('achieve_id', None)
        params['ad'] = "appdriver紅利"
        params['order'] = "appdriver紅利"
        params['getPoint'] = int(float(self.get_argument('point', "")))
        detail = 'aos'
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s AND `appType`=0",
            params['scopeid'])
        if not uid:
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['scopeid'])
            return
        cheat = self.db.get(
            "SELECT points, count(*) FROM `callback_order` WHERE `user` = %s  AND `ad_source` = '110' AND DATE(`time`)=CURDATE() ",
            uid['uid'])
        if cheat:
            if cheat['count(*)'] < 4:
                self.saveOrder(
                    uid['uid'], params['order'], params['ad'], params['adid'], params['scopeid'], 0,
                    params['getPoint'], 0, 0, params['device'], 0, 110, 3, detail)
                self.push(params['scopeid'],params['ad'],params['getPoint'])
                self.pushEng(params['scopeid'],params['ad'],params['getPoint'])
                self.pushIosAppstore(params['scopeid'],params['ad'],params['getPoint'])
            else:
                self.pushoverWarn(uid['uid'])

    def pushoverWarn(self,uid):
        """Pushover针对appdriver作弊报警"""
        import urllib
        conn = httplib.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
            urllib.urlencode({
                "token": self.config['pushover']['token'],
                "user": self.config['pushover']['user'],
                "message": "uid"+str(uid)+"作弊",
            }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()

    def __save_trialpay_order(self):
        params = {}
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1 LIMIT 1", self.ip)
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            return
        params['scopeid'] = self.get_argument('sid', None)
        params['adid'] = self.get_argument('oid', None)
        params['ad'] = "trialpay紅利"
        params['order'] = "trialpay紅利"
        params['getPoint'] = self.get_argument('reward_amount', "")
        detail = 'aos'
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s AND `appType`=0",
            params['scopeid'])
        if not uid:
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['scopeid'])
            return
        self.saveOrder(
            uid['uid'], params['order'], params['ad'], params['adid'], params['scopeid'], 0,
            params['getPoint'], 0, 0, 0, 0, 109, 3, detail)
        self.push(params['scopeid'],params['ad'],params['getPoint'])
        self.pushEng(params['scopeid'],params['ad'],params['getPoint'])
        self.pushIosAppstore(params['scopeid'],params['ad'],params['getPoint'])

    def __save_appdriver_ios_order(self):
        params = {}
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1 LIMIT 1", self.ip)
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            return
        params['scopeid'] = self.get_argument('identifier', None)
        params['device'] = self.get_argument('idfa', None)
        params['adid'] = self.get_argument('achieve_id', None)
        params['ad'] = "appdriver紅利"
        params['order'] = "appdriver紅利"
        params['getPoint'] = int(float(self.get_argument('point', "")))
        detail = 'ios'
        # print params['getPoint']
        # print 'pt'
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s AND `appType`=0",
            params['scopeid'])
        if not uid:
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['scopeid'])
            return
        cheat = self.db.get(
            "SELECT points, count(*) FROM `callback_order` WHERE `user` = %s  AND `ad_source` = '110' AND DATE(`time`)=CURDATE() ",
            uid['uid'])
        if cheat:
            if cheat['count(*)'] < 4:
                self.saveOrder(
                    uid['uid'], params['order'], params['ad'], params['adid'], params['scopeid'], 0,
                    params['getPoint'], 0, 0, params['device'], 0, 110, 5, detail)
                self.push(params['scopeid'],params['ad'],params['getPoint'])
                self.pushEng(params['scopeid'],params['ad'],params['getPoint'])
                self.pushIosAppstore(params['scopeid'],params['ad'],params['getPoint'])
            else:
                self.pushoverWarn(uid['uid'])
                # print "cheat"

    def __save_youmi_order(self):
        params = {}
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        if self.ip == '58.63.244.57' or self.ip =='58.63.244.58' or self.ip == '54.64.29.23':
            pass
        else:
            self.ip = "&ERRip="+str(self.ip)
            #return
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1 LIMIT 1", self.ip)
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            return
        params['scopeid'] = self.get_argument('user', None)
        params['app'] = self.get_argument('app', None)
        params['pkg'] = self.get_argument('pkg', '')
        params['chn'] = self.get_argument('chn', None)
        params['device'] = self.get_argument('device', '')
        params['timestamp'] = self.get_argument('time', None)
        params['adid'] = self.get_argument('adid', '')
        params['sig'] = self.get_argument('sig', None)
        params['trade_type']=self.get_argument('trade_type', '')
        params['order'] = self.get_argument('order', None)
        detail = " aos ( 应用名:"+self.get_argument('ad', None)+" |包名:"+params['pkg']+ \
            " |imei:"+params['device']+" |任务id:"+params['adid']+" |步骤:"+params['trade_type']+" )"
        params['ad'] = "有米紅利"
        params['getPoint'] = self.get_argument('points', "")
        params['price'] = self.get_argument('price', None)
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s AND `appType`=0",
            params['scopeid'])
        if not uid:
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['scopeid'])
            return
        info = self.db.get(
            "SELECT * FROM `callback_order` WHERE `user`=%s and `order`=%s and `ad_source`=107 LIMIT 1",
            uid['uid'],params['order'])
        if not info:
            self.saveOrder(
                uid['uid'], params['order'], params['ad'], params['adid'], params['scopeid'], params['chn'],
                params['getPoint'], params['price'], 0, params['device'], params['sig'], 107, 3, detail)
            self.push(params['scopeid'],params['ad'],params['getPoint'])
            self.pushIosAppstore(params['scopeid'],params['ad'],params['getPoint'])
            self.pushEng(params['scopeid'],params['ad'],params['getPoint'])

    def __save_youmiios_order(self):
        params = {}
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        if self.ip == '58.63.244.57' or self.ip =='58.63.244.58' or self.ip == '54.64.29.23':
            pass
        else:
            self.ip = "&ERRip="+str(self.ip)
            return
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1 LIMIT 1", self.ip)
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            return
        params['scopeid'] = self.get_argument('user', "")
        params['order'] = self.get_argument('order', None)
        params['app'] = self.get_argument('app', None)
        params['chn'] = self.get_argument('chn', None)
        params['device'] = self.get_argument('device', None)
        params['timestamp'] = self.get_argument('time', None)
        params['adid'] = self.get_argument('adid', None)
        params['sig'] = self.get_argument('sig', None)
        params['storeid'] = self.get_argument('storeid', None)
        params['ad'] = "有米紅利"
        params['getPoint'] = self.get_argument('points', "")
        detail = " ios ( 应用名:"+self.get_argument('ad', None)+" |adid="+params['adid']+ \
            " |device="+params['device']+" |storeid="+params['storeid']+" )"
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s AND `appType`=0",
            params['scopeid'])
        if not uid:
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['scopeid'])
            return
        info = self.db.get(
            "SELECT * FROM `callback_order` WHERE `user`=%s and `order`=%s and `ad_source`=107 LIMIT 1",
            uid['uid'],params['order'])
        if not info and params['scopeid']!="":
            self.saveOrder(
                uid['uid'], params['order'], params['ad'], params['adid'], params['scopeid'], params['chn'],
                params['getPoint'], 0, 0, params['device'], params['sig'], 107, 5, detail)
            self.push(params['scopeid'],params['ad'],params['getPoint'])
            self.pushEng(params['scopeid'],params['ad'],params['getPoint'])
            self.pushIosAppstore(params['scopeid'],params['ad'],params['getPoint'])

    def __save_adcolony_order(self):
        params = {}
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1 LIMIT 1", self.ip)
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            return
        params['scopeid'] = self.get_argument('custom_id', '')
        params['ad'] = "adcolony紅利"
        params['order'] = "adcolony紅利"
        params['getPoint'] = int(float(self.get_argument('amount', "")))
        params['trans_id'] = self.get_argument('id', '')
        params['dev_id'] = self.get_argument('uid', '')
        params['currency'] = self.get_argument('currency', '')
        params['verifier'] = self.get_argument('verifier', '')
        params['key'] = "v4vcc3562d7323cb476ba1"
        detail = 'aos'
        #secret_key = MD5 hash 值
        #简单防欺诈
        valild =  "" + params['trans_id'] + params['dev_id'] + str(params['getPoint']) + params['currency'] + params['key'] +params['scopeid']
        self.valild_str =  hashlib.md5(valild).hexdigest()
        if self.valild_str!=params['verifier']:
            self.write('vc_decline')
            return
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s AND `appType`=0",
            params['scopeid'])
        if uid==None:
            self.write('vc_decline')
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['scopeid'])
            return
        cheat = self.db.get(
            "SELECT points, count(*) FROM `callback_order` WHERE `user` = %s  AND `ad_source` = '113' AND DATE(`time`)=CURDATE() ",
            uid['uid'])
        if cheat:
            if cheat['count(*)'] < 10:
                self.saveOrder(
                    uid['uid'], params['order'], params['ad'], params['trans_id'], params['scopeid'], 0,
                    params['getPoint'], 0, 0, params['dev_id'], 0, 113, 3, detail)
                self.push(params['scopeid'],params['ad'],params['getPoint'])
                self.pushEng(params['scopeid'],params['ad'],params['getPoint'])
                self.pushIosAppstore(params['scopeid'],params['ad'],params['getPoint'])
                self.write('vc_success')
            else:
            #    self.pushoverWarn(uid['uid'])
                self.write('vc_decline')

    def __save_flurry_order(self):
        params = {}
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1 LIMIT 1", self.ip)
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            return
        params['scopeid'] = self.get_argument('userid', None)
        params['order'] = "flurry紅利"
        params['fguid'] = self.get_argument('fguid', None)
        params['ad'] = "flurry紅利"
        params['getPoint'] = self.get_argument('rewardquantity', "")
        # GetVerifier = self.get_argument('fhash', "")
        detail = 'aos'
        params['key'] = '385DY4B2VNKZFXZF57YP'
        #secret_key = MD5 hash 值
        #简单防欺诈
        valild = params['fguid'] + ":" + params['getPoint'] + ":" + params['key']
        self.valild_str = hashlib.md5(valild).hexdigest()
        # print self.valild_str
        # print GetVerifier
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s AND `appType`=0",
            params['scopeid'])
        if not uid:
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['scopeid'])
            return
        self.saveOrder(
            uid['uid'], params['order'], params['ad'], 0, params['scopeid'], 0,
            params['getPoint'], 0, 0, '', 0, 114, 3, detail)
        self.push(params['scopeid'],params['ad'],params['getPoint'])
        self.pushEng(params['scopeid'],params['ad'],params['getPoint'])
        self.pushIosAppstore(params['scopeid'],params['ad'],params['getPoint'])

    def __save_appdriveros_order(self):
        params = {}
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        if self.ip == '54.251.141.1' or self.ip =='54.251.161.122':
            pass
        else:
            self.ip = "&ERRip="+str(self.ip)
            self.write('0')
            return
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1 LIMIT 1", self.ip)
        params['ad'] = "appdriver紅利"
        params['getPoint'] = self.get_argument('point', "")
        params['scopeid'] = self.get_argument('identifier', '')
        params['timestamp'] = self.get_argument('accepted_time', '')
        params['server_ip'] = self.get_argument('Userip', '')
        params['adid'] = self.get_argument('achieve_id', '')
        params['advertisement_name']=self.get_argument('advertisement_name', '')
        params['order'] = self.get_argument('campaign_name', '')
        params['advertisement_id'] = self.get_argument('advertisement_id','')
        detail = " aos ( 应用名:"+params['order']+" |获取方式:"+params['advertisement_name']+ \
                " |任务唯一id:"+params['adid']+" |媒体id:"+params['advertisement_id']+" )"
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            self.write('0')
            return
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s AND `appType`=0",
            params['scopeid'])
        if not uid:
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['scopeid'])
            return
        info = self.db.get(
            "SELECT * FROM `callback_order` WHERE `user`=%s and `order`=%s \
            and `adid`= %s and `ad_source`=110 LIMIT 1",
            uid['uid'], params['order'], params['adid'])
        if not info:
            self.saveOrder(
                uid['uid'], params['order'], params['ad'], params['adid'], params['scopeid'], 0,
                params['getPoint'], 0, params['timestamp'], 0, 0, 110, 3, detail)
            self.push(params['scopeid'],params['ad'],params['getPoint'])
            self.pushEng(params['scopeid'],params['ad'],params['getPoint'])
            self.pushIosAppstore(params['scopeid'],params['ad'],params['getPoint'])
            self.write('1')
        else:
            self.write('0')

    def __save_fyber_order(self):
        params = {}
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1 LIMIT 1", self.ip)
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            return
        params['scopeid'] = self.get_argument('uid', None)
        params['order'] = "fyber紅利"
        params['device'] = self.get_argument('sid', None)
        params['ad'] = "fyber紅利"
        params['getPoint'] = self.get_argument('amount', "")
        params['adid']= self.get_argument('_trans_id_', '')
        detail = 'aos'
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s AND `appType`=0",
            params['scopeid'])
        if not uid:
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['scopeid'])
            return
        info = self.db.get("SELECT * FROM `callback_order` WHERE `user` = %s AND `adid` = %s AND `points`= %s", \
                           uid['uid'], params['adid'], int(params['getPoint']))
        if not info:
            self.saveOrder(
                uid['uid'], params['order'], params['ad'], params['adid'], params['scopeid'], 0,
                params['getPoint'], 0, 0, params['device'], 0, 108, 3, detail)
            self.push(params['scopeid'],params['ad'],params['getPoint'])
            self.pushEng(params['scopeid'],params['ad'],params['getPoint'])
            self.pushIosAppstore(params['scopeid'],params['ad'],params['getPoint'])
        else:
            pass

    def __save_fyberios_order(self):
        params = {}
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1 LIMIT 1", self.ip)
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            return
        params['scopeid'] = self.get_argument('uid', None)
        params['order'] = "fyber紅利"
        params['device'] = self.get_argument('sid', None)
        params['ad'] = "fyber紅利"
        params['getPoint'] = self.get_argument('amount', "")
        params['adid']= self.get_argument('_trans_id_', '')
        detail = 'ios'
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s AND `appType`=0",
            params['scopeid'])
        if not uid:
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['scopeid'])
            return
        info = self.db.get("SELECT * FROM `callback_order` WHERE `user` = %s AND `adid` = %s AND `points`= %s", \
                           uid['uid'], params['adid'], int(params['getPoint']))
        if not info:
            self.saveOrder(
                uid['uid'], params['order'], params['ad'], params['adid'], params['scopeid'], 0,
                params['getPoint'], 0, 0, params['device'], 0, 108, 5, detail)
            self.push(params['scopeid'],params['ad'],params['getPoint'])
            self.pushEng(params['scopeid'],params['ad'],params['getPoint'])
            self.pushIosAppstore(params['scopeid'],params['ad'],params['getPoint'])

    def __save_vungle_order(self):
        params = {}
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1 LIMIT 1", self.ip)
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            return
        params['scopeid'] = self.get_argument('uid', "")
        params['order'] = "vungle紅利"
        params['device'] = self.get_argument('openudid', "")
        params['ad'] = "vungle紅利"
        params['getPoint'] = self.get_argument('amount', "")
        params['adid'] = self.get_argument('txid', "")
        token = self.get_argument('digest', "")
        detail = 'aos'
        key = "49XqHzUfhZYPU8AmgL0iZQhX6ebpQcx/JT8HBUoK+Ng="
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s AND `appType`=0",
            params['scopeid'])
        if not uid:
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['scopeid'])
            return
        info = self.db.get(
            "SELECT * FROM `callback_order` WHERE `user` = %s  AND `ad_source` = '106' AND `adid`=%s",
            uid['uid'], params['adid'])
        firsthash = hashlib.sha256()
        firsthash.update(key + ":" + params['adid'])
        secondhash = hashlib.sha256()
        secondhash.update(firsthash.digest())
        if secondhash.hexdigest() != token:
            return
        if not info:
            self.saveOrder(
                uid['uid'], params['order'], params['ad'], params['adid'], params['scopeid'], 0,
                params['getPoint'], 0, 0, params['device'], 0, 106, 3, detail)
            self.push(params['scopeid'],params['ad'],params['getPoint'])
            self.pushEng(params['scopeid'],params['ad'],params['getPoint'])
            self.pushIosAppstore(params['scopeid'],params['ad'],params['getPoint'])

    def __save_tokenads_order(self):
        params = {}
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1 LIMIT 1", self.ip)
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            return
        params['scopeid'] = self.get_argument('uid', None)
        params['order'] = "woobi紅利"
        params['adid'] = self.get_argument('transaction_id', None)
        params['ad'] = "woobi紅利"
        params['getPoint'] = int(float(self.get_argument('award', "")))
        params['client_ip'] = self.get_argument('client_ip', "")
        clientip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1 LIMIT 1", params['client_ip'])
        if clientip_info:
            self.ip = "&ERRip="+str(self.ip)
            return
        hash = self.get_argument('hash', "")
        sign = self.get_argument('sign', "")
        detail = 'aos'
        params['key'] = '47d70b4e60b54dac'
        #secret_key = MD5 hash 值
        #简单防欺诈
        valid = hash + params['key']
        valid_str = hashlib.md5(valid).hexdigest()
        if valid_str != sign:
            return
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s AND `appType`=0",
            params['scopeid'])
        if not uid:
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['scopeid'])
            return
        info = self.db.get(
            "SELECT * FROM `callback_order` WHERE `user` = %s  AND `ad_source` = '115' AND `adid`=%s LIMIT 1",
            uid['uid'], params['adid'])
        if not info:
            self.saveOrder(
                uid['uid'], params['order'], params['ad'], params['adid'], params['scopeid'], 0,
                params['getPoint'], 0, 0, '', 0, 115, 3, detail)
            self.push(params['scopeid'],params['ad'],params['getPoint'])
            self.pushEng(params['scopeid'],params['ad'],params['getPoint'])
            self.pushIosAppstore(params['scopeid'],params['ad'],params['getPoint'])


    def __save_duomeng_order(self):
        params = {}
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1", self.ip)
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            # return
        params['action'] = self.get_argument('action', '').encode('utf-8')
        params['action_name'] = self.get_argument('action_name', '').encode('utf-8')
        params['ad'] = self.get_argument('ad', '').encode('utf-8')
        params['adid'] = self.get_argument('adid', '').encode('utf-8')
        params['channel'] = self.get_argument('channel', '').encode('utf-8')
        params['device'] = self.get_argument('device', '').encode('utf-8')
        params['orderid'] = self.get_argument('orderid', '').encode('utf-8')
        params['pkg'] = self.get_argument('pkg', '').encode('utf-8')
        params['point'] = self.get_argument('point', '').encode('utf-8')
        params['price'] = self.get_argument('price', '').encode('utf-8')
        params['pubid'] = self.get_argument('pubid', '').encode('utf-8')
        params['ts'] = self.get_argument('ts', '').encode('utf-8')
        params['user'] = self.get_argument('user', '').encode('utf-8')
        params['order'] = "duomeng紅利"
        #params['key'] = '940db0e6'
        params['key'] = ("234629bc").encode('utf-8')
        self.valild_str = utils.md5_sign(params)
        verifier = self.get_argument('sign', '')
        detail = " aos ( 应用名:"+params['ad']+ " |任务唯一id:"+params['orderid'] + " )"
        #print params
        #secret_key = MD5 hash 值
        #简单防欺诈
        #valild =  "action=" + params['action'] + "action_name=" + params['action_name'] + \
        #    "ad="+ params['ad']+"adid="+params['adid'] + "channel="+ str(params['channel']) + \
        #    "device=" + params['device'] + "orderid=" + params['orderid'] + "pkg=" + params['pkg'] + \
        #    "point=" + params['point'] + "price" + params['price'] + "pubid=" + params['pubid'] + \
        #    "ts=" + params['ts'] + "user=" + params['user'] + params['key']
        #print valild
        #self.valild_str =  hashlib.md5(valild).hexdigest()
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s and `appType`=0",
            params['user'])
        if uid==None:
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['user'])
            #return
        orderinfo = self.db.get(
            "SELECT * FROM `callback_order` WHERE `ad_source`=117 AND `adid`=%s AND `user`=%s LIMIT 1", params['orderid'], uid['uid'])
        if not orderinfo:
            self.saveOrder(
                uid['uid'], params['order'], params['order'], params['orderid'], params['user'], params['channel'],
                params['point'], params['price'], params['ts'], params['device'], verifier, 117, 3, detail)
            self.push(params['user'],params['order'],params['point'])
            self.pushEng(params['user'],params['order'],params['point'])

    def __save_iosduomeng_order(self):
        params = {}
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1", self.ip)
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            # return
        params['action'] = self.get_argument('action', '').encode('utf-8')
        params['action_name'] = self.get_argument('action_name', '').encode('utf-8')
        params['ad'] = self.get_argument('ad', '').encode('utf-8')
        params['adid'] = self.get_argument('adid', '').encode('utf-8')
        params['channel'] = self.get_argument('channel', '').encode('utf-8')
        params['device'] = self.get_argument('device', '').encode('utf-8')
        params['orderid'] = self.get_argument('orderid', '').encode('utf-8')
        params['pkg'] = self.get_argument('pkg', '').encode('utf-8')
        params['point'] = self.get_argument('point', '').encode('utf-8')
        params['price'] = self.get_argument('price', '').encode('utf-8')
        params['pubid'] = self.get_argument('pubid', '').encode('utf-8')
        params['ts'] = self.get_argument('ts', '').encode('utf-8')
        params['user'] = self.get_argument('user', '').encode('utf-8')
        params['order'] = "duomeng紅利"
        #params['key'] = '940db0e6'
        params['key'] = ("234629bc").encode('utf-8')
        self.valild_str = utils.md5_sign(params)
        verifier = self.get_argument('sign', '')
        detail = " ios ( 应用名:"+params['ad']+ " |任务唯一id:"+params['orderid'] + " )"
        #print params
        #secret_key = MD5 hash 值
        #简单防欺诈
        #valild =  "action=" + params['action'] + "action_name=" + params['action_name'] + \
        #    "ad="+ params['ad']+"adid="+params['adid'] + "channel="+ str(params['channel']) + \
        #    "device=" + params['device'] + "orderid=" + params['orderid'] + "pkg=" + params['pkg'] + \
        #    "point=" + params['point'] + "price" + params['price'] + "pubid=" + params['pubid'] + \
        #    "ts=" + params['ts'] + "user=" + params['user'] + params['key']
        #print valild
        #self.valild_str =  hashlib.md5(valild).hexdigest()
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s and `appType`=0",
            params['user'])
        if uid==None:
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['user'])
            #return
        orderinfo = self.db.get(
            "SELECT * FROM `callback_order` WHERE `ad_source`=117 AND `adid`=%s AND `user`=%s LIMIT 1", params['orderid'], uid['uid'])
        if not orderinfo:
            self.saveOrder(
                uid['uid'], params['order'], params['order'], params['orderid'], params['user'], params['channel'],
                params['point'], params['price'], params['ts'], params['device'], verifier, 117, 3, detail)
            self.push(params['user'],params['order'],params['point'])
            self.pushEng(params['user'],params['order'],params['point'])
            self.pushIosAppstore(params['user'],params['ad'],params['point'])

    def __save_adxmi_order(self):
        params = {}
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1", self.ip)
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            return
        self.params={}
        params['sign'] = self.get_argument('sign', '')
        kv = self.request.arguments
        from urllib import unquote
        for k in kv:
            if k != 'sign':
                self.params[k] = unquote(kv[k][0]).encode('utf-8')
            # 排序
        token = '9a4e2073bytrcnmi'
        if  utils.md5_gofreeadxmisign(self.params, token) != params['sign']:
            self.ip = "&ERRSign"+str(self.ip)
            # return
        params['scopeid'] = self.get_argument('user', '')
        params['app'] = self.get_argument('app', '')
        params['pkg'] = self.get_argument('pkg', '')
        params['chn'] = self.get_argument('chn', '0')
        params['device'] = self.get_argument('device', '')
        params['timestamp'] = self.get_argument('time', '')
        params['adid'] = self.get_argument('adid', '')
        params['sig'] = self.get_argument('sig', '')
        params['order'] = self.get_argument('order', '')
        detail = " aos ( 应用名:"+self.get_argument('ad', '')+" |包名:"+params['pkg']+ \
            " |imei:"+params['device']+" |任务id:"+params['adid']+" )"
        params['ad'] = "adxmi紅利"
        params['getPoint'] = self.get_argument('points', "")
        params['price'] = self.get_argument('revenue', '')
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s",
            params['scopeid'])
        if not uid:
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['scopeid'])
            return
        info = self.db.get(
            "SELECT * FROM `callback_order` WHERE `user`=%s and `order`=%s and `ad_source`=119 LIMIT 1",
            uid['uid'],params['order'])
        if not info:
            self.saveOrder(
                uid['uid'], params['order'], params['ad'], params['adid'], params['scopeid'], 0,
                params['getPoint'], params['price'], 0, params['device'], params['sig'], 119, 3, detail)
            self.push(params['scopeid'],params['ad'],params['getPoint'])

    def __save_adxmiios_order(self):
        params = {}
        self.ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1", self.ip)
        if ip_info:
            self.ip = "&ERRip="+str(self.ip)
            return
        self.params={}
        params['sign'] = self.get_argument('sign', '')
        kv = self.request.arguments
        from urllib import unquote
        for k in kv:
            if k != 'sign':
                self.params[k] = unquote(kv[k][0]).encode('utf-8')
            # 排序
        token = '748eca1fec9cdf14'
        if  utils.md5_gofreeadxmisign(self.params, token) != params['sign']:
            self.ip = "&ERRSign"+str(self.ip)
            # return
        params['scopeid'] = self.get_argument('user', '')
        params['app'] = self.get_argument('app', '')
        params['pkg'] = self.get_argument('pkg', '')
        params['chn'] = self.get_argument('chn', '0')
        params['device'] = self.get_argument('device', '')
        params['timestamp'] = self.get_argument('time', '')
        params['adid'] = self.get_argument('adid', '')
        params['sig'] = self.get_argument('sig', '')
        params['order'] = self.get_argument('order', '')
        detail = " ios ( 应用名:"+self.get_argument('ad', '')+" |包名:"+params['pkg']+ \
            " |imei:"+params['device']+" |任务id:"+params['adid']+" )"
        params['ad'] = "adxmi紅利"
        params['getPoint'] = self.get_argument('points', "")
        params['price'] = self.get_argument('revenue', '')
        uid=self.db.get(
            "SELECT `uid` FROM `user` WHERE `scopeid`=%s",
            params['scopeid'])
        if not uid:
            return
        black_user = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid` = %s AND `status`=1 LIMIT 1", uid['uid'])
        if black_user:
            self.ip = "&BlackUser="+str(params['scopeid'])
            return
        info = self.db.get(
            "SELECT * FROM `callback_order` WHERE `user`=%s and `order`=%s and `ad_source`=119 LIMIT 1",
            uid['uid'],params['order'])
        if not info:
            self.saveOrder(
                uid['uid'], params['order'], params['ad'], params['adid'], params['scopeid'], 0,
                params['getPoint'], params['price'], 0, params['device'], params['sig'], 119, 3, detail)
            self.push(params['scopeid'],params['ad'],params['getPoint'])

    #所有平台存入数据库
    def saveOrder(
            self, uid, order, ad, adid, scopeid, chn, points,
            price, time, device, sig, ad_source, platform, detail):
        """保存订单"""
        # todo 使用事务 log
        user_info = {}
        user_info = self.db.get(
            "SELECT * FROM `user` WHERE `uid` = %s", uid)
        oid = self.db.execute_lastrowid(
            "INSERT INTO `global_orders` (uid, points, last, type, note)"
            "VALUES (%s, %s, %s, %s, %s)",
            uid, points, user_info['points'], 6, ad+detail)

        self.db.execute(
            'INSERT INTO  `callback_order` (`order`, `oid`, `ad`,\
            `adid`, `user`, `chn`, `points`, `price`, `device`,\
            `sig`, `platform`, `ad_source`) '
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            order, oid, ad, adid, uid, chn, points, price, device, sig,platform, ad_source)

        self.db.execute(
            "UPDATE  `user` SET  `points` = `points` + %s,\
            `total_points` = `total_points` + %s "
            "WHERE `user`.`uid` = %s", points, points, uid)
        self.earnPoint(uid, order, ad, adid, scopeid, chn, points,
            price, time, device, sig, ad_source, platform, detail)

    def push(self,scopeid,adName,point):
        """推送到Parse"""
        connection = httplib.HTTPSConnection('api.parse.com', 443)
        connection.connect()
        connection.request('POST', '/1/push', json.dumps({
            "where": {
                 "scopeid": ""+scopeid+""
            },
            "data": {
                 "action": 2,
                 "alert": "恭喜，您獲得了"+adName+str(point)+"點"
            }
            }), {
            "X-Parse-Application-Id": self.config['push']['ApplicationId'],
            "X-Parse-REST-API-Key": self.config['push']['APIKey'],
            "Content-Type": "application/json"
             })
    def pushEng(self,scopeid,adName,point):
        """推送到Parse"""
        connection = httplib.HTTPSConnection('api.parse.com', 443)
        connection.connect()
        connection.request('POST', '/1/push', json.dumps({
            "where": {
                 "scopeid": ""+scopeid+"",
                 "language": "en"
            },
            "data": {
                 "action": 2,
                 "alert": "Congratulations, you got"+adName+str(point)+"point"
            }
            }), {
            "X-Parse-Application-Id": 'QId0viozmHUmvUls21u6iQZjjOu8BOui7lCVpTIj',
            "X-Parse-REST-API-Key": 'mTRFga2YIGlI8cFMahoZimMXIejzNBRImDH3qdLV',
            "Content-Type": "application/json"
             })

    def pushIosAppstore(self,scopeid,adName,point):
        """IosAppStore版推送到Parse"""
        connection = httplib.HTTPSConnection('api.parse.com', 443)
        connection.connect()
        connection.request('POST', '/1/push', json.dumps({
            "where": {
                 "scopeid": ""+scopeid+""
            },
            "data": {
                 "action": 2,
                 "alert": "恭喜，您獲得了"+adName+str(point)+"點"
            }
            }), {
            "X-Parse-Application-Id": self.config['pushIosAppstore']['ApplicationId'],
            "X-Parse-REST-API-Key": self.config['pushIosAppstore']['APIKey'],
            "Content-Type": "application/json"
             })

    def getSign(self):
        array1=self.db.query("select * from callback_order where ad_source =4 and points <> 30 ");
        array2=self.db.query("select * from callback_order where ad_source=4 and points=5 ");
        arr = []
        user = []
        time = []
        point = []
        datas = []
        for ary1 in array1:
            for ary2 in array2:
                if (ary1['user']==ary2['user'] and (ary2['time']-ary1['time'])<datetime.timedelta(1) and (ary2['time']-ary1['time'])!=datetime.timedelta(0) and
                    (ary2['time']>ary1['time'])
                    and (ary1['time']-ary2['time'])!=datetime.timedelta(0)
                    ):
                    if((ary2['time']+datetime.timedelta(hours=8))
                        -(ary1['time']+datetime.timedelta(hours=8))
                       !=(datetime.timedelta(days=0))):
                        vo = ary2.copy()
                        if vo.get("time"):
                            vo['time'] = (vo.get('time')+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
                        else:
                            print "no time find"
                        dic = {
                            'user': vo['user'],
                            'time': vo['time'],
                            'points': vo['points'],
                        }
                        datas.append(dic)
                        arr.append(vo)
                        user.append(str(vo['user']))
                        time.append(vo['time'])
                        point.append(vo['points'])
        self.user = user
        self.time = time
        self.point = point
        self.datas = datas

    def getSupersonicRepeat(self):
        array1=self.db.query("select * from callback_order where ad_source = 104");
        array2=self.db.query("select * from callback_order where ad_source = 104");
        arr = []
        user = []
        time = []
        point = []
        datas = []
        for ary1 in array1:
            for ary2 in array2:
                if (ary1['user']==ary2['user'] and (ary2['points']==ary1['points']) and (ary2['time']-ary1['time'])<datetime.timedelta(seconds=601) and ary2['time']>ary1['time']):
                        dic = {
                            'user': ary2['user'],
                            'time': ary2['time'],
                            'points': ary2['points'],
                        }
                        self.write(str(ary2['user'])+",")
                        datas.append(dic)
                        arr.append(ary2)
                        user.append(str(ary2['user']))
                        time.append(ary2['time'])
                        point.append(ary2['points'])
        self.user = user
        self.time = time
        self.point = point
        self.datas = datas

    def getPaypoint(self):
        with open('user.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for line in spamreader:
                user_info = {}
                user_info = self.db.get(
                    "SELECT * FROM `user` WHERE `uid` = %s", line[0])
                if user_info:
                    oid = self.db.execute_lastrowid(
                        "INSERT INTO `global_orders` (uid, points, last)"
                        "VALUES (%s, %s, %s)",
                        line[0], 30, user_info['points'])
                    order = "簽到補償"
                    ad ="簽到補償"
                    self.db.execute(
                        'INSERT INTO  `callback_order` (`order`, `oid`, `ad`,\
                        `adid`, `user`, `chn`, `points`, `price`, `device`,\
                        `sig`, `platform`, `ad_source`) '
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 3, %s)",
                        order, oid, ad, 0, line[0], 0, 30, 0, 0, 0, 4)

                    self.db.execute(
                        "UPDATE  `user` SET  `points` = `points` + %s,\
                        `total_points` = `total_points` + %s "
                        "WHERE `user`.`uid` = %s", 30, 30, line[0])

    def __log(self,ip):
        """回调打log"""
        if not self.logger:
	    #日志记录的用例名
            self.logger = logging.getLogger('my')
            self.logger.setLevel(logging.INFO)
	    #文件名
            fh = logging.FileHandler(self.config['log']['callback_log'])
            fh.setLevel(logging.INFO)

            formatter = logging.Formatter('%(asctime)s - %(message)s')
            fh.setFormatter(formatter)
            if not self.logger.handlers:
                self.logger.addHandler(fh)

        self.logger.info(self.request.uri+"&Userip="+ip)

    #淩晨守鐘幸運獎勵
    def earnPoint(self, uid, order, ad, adid, scopeid, chn, points,
            price, time, device, sig, ad_source, platform, detail):
        import random, time
        timestamp = int(time.time())
        flag = False
        #flag = True
        if (1430841600<=timestamp<=1430843400) or \
            (1431100800<=timestamp<=1431102600) or \
            (1431446400<=timestamp<=1431448200) or \
            (1431705600<=timestamp<=1431707400) or \
            (1432051200<=timestamp<=1432053000) or \
            (1432310400<=timestamp<=1432312200) or \
            (1432656000<=timestamp<=1432657800) or \
            (1432915200<=timestamp<=1432917000) or \
            (1430708400<=timestamp<=1430710200):
            flag = True
        getpoint = 0
        if int(uid)==6456 or int(uid)==101021:
            flag = True
        if int(points)>19 and flag==True:
            value = random.randint(1,100)
            if 0<=value<=60:
                getpoint = int(int(points)*0.05)
            elif 61<=value<=90:
                getpoint = int(int(points)*0.15)
            elif 91<=value<=100:
                getpoint = int(int(points)*0.25)
            user_info = {}
            ad=order=u"夜貓福利"
            user_info = self.db.get(
                "SELECT * FROM `user` WHERE `uid` = %s", uid)
            oid = self.db.execute_lastrowid(
                "INSERT INTO `global_orders` (uid, points, last, type, note)"
                "VALUES (%s, %s, %s, %s, %s)",
                uid, getpoint, user_info['points'], 17, ad)
            self.db.execute(
                'INSERT INTO  `callback_order` (`order`, `oid`, `ad`,\
                `adid`, `user`, `chn`, `points`, `price`, `device`,\
                `sig`, `platform`, `ad_source`) '
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                order, oid, ad, adid, uid, chn, getpoint, price, device, sig,platform, 17)
            self.db.execute(
                "UPDATE  `user` SET  `points` = `points` + %s,\
                `total_points` = `total_points` + %s "
                "WHERE `user`.`uid` = %s", getpoint, getpoint, uid)
            msg = u"【夜貓福利】恭喜您獲得額外獎勵:"
            utils.earnPush(self,scopeid, msg, int(getpoint))


