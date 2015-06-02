#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

用户相关
@author zhenyong, lisongjian@youmi.net

"""

#import requests
import protocols
import constants
import time
import string
import random
import hashlib
import json,urllib2
import datetime
import utils
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class UserHandler(protocols.JSONBaseHandler):
    """ aos用户创建以及信息查询 """

    @protocols.unpack_arguments_bytoken(with_token=False)
    def post(self):
        # H7hLcmuAhCZOZYT2zJTv6+ouY9Wtu+RomKkaaMrBG2MWouL9YixIC/LrVf6ekk8v
        pname = self.arguments.get('pname',"")
        channel = self.arguments.get('channel',"")
        params = {}
        for key in ['ei', 'si', 'andid', 'mac', 'rt', 'scopeid', \
            'utm_campaign', 'utm_source', 'utm_medium', 'utm_content', 'utm_term']:
            params[key] = self.arguments.get(key, "")
        #print params['scopeid']

        fingerprinting = self.__get_devicefingerprinting(params)
        # print params
        ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1 LIMIT 1", ip)
        cheat = 0
        cheatType = 0
        if ip_info:
            cheat = 1
            cheatType = 1
        imei_info = self.db.get("SELECT * FROM `imei_blacklist` WHERE `imei` = %s AND `imei`!= 'null' \
                                AND `status`=1 LIMIT 1", params['ei'])
        if imei_info:
            cheat = 1
            cheatType = 2
        user_device = self.db.get(
            "SELECT `sid`, `fingerprinting` from `user_device` \
            where `fingerprinting` = %s LIMIT 1",
            fingerprinting)
        #print params
        #print fingerprinting
        if not user_device:
            # 新增一个设备id
            sid = self.db.execute_lastrowid(
                "INSERT INTO `user_device` (`ei`, `si`, `mac`, `andid`,\
                `fingerprinting`,`ip`, `cheat`, `type`, \
                `utm_campaign`, `utm_source`, `utm_medium`, `utm_content`, `utm_term`)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, \
                %s, %s, %s, %s, %s)",
                params['ei'], params['si'], params['mac'], params['andid'],fingerprinting,ip,int(cheat),int(cheatType), \
                params['utm_campaign'], params['utm_source'], params['utm_medium'], params['utm_content'], params['utm_term'])
        else:
            self.db.execute(
                "UPDATE `user_device` set `cheat` =  %s,\
                `ip` =  %s, \
                `ei` = %s, \
                `type` = %s \
                WHERE `fingerprinting` = %s", cheat, ip, params['ei'], cheatType, fingerprinting)
        # tapjoy/fyber推广阈值
        tapjoy_points = self.db.get("SELECT `values` FROM `options` WHERE `key`='campaign_threshold'")
        fyber_points = self.db.get("SELECT `values` FROM `options` WHERE `key`='fyber_campaign_threshold'")
        self.return_result({
            "token": fingerprinting,
            "campaign_threshold": tapjoy_points['values'],
            "fyber_campaign_threshold": fyber_points['values'],
            "pname": pname,
            "channel": channel,
            })

    def __get_devicefingerprinting(self, device_params):
        """简单的生成设备指纹方法"""
        valid_params = [
            device_params['ei'],
            device_params['si'],
            device_params['mac'],
            device_params['andid'],
        ]
        device_str = ':'.join(str(valid_params))
        #print device_str
        return hashlib.md5(device_str).hexdigest()



class UseriosHandler(protocols.JSONBaseHandler):
    """ ios用户创建以及信息查询 """

    @protocols.unpack_arguments_bytoken(with_token=False)
    def post(self):
        # H7hLcmuAhCZOZYT2zJTv6+ouY9Wtu+RomKkaaMrBG2MWouL9YixIC/LrVf6ekk8v
        pname = self.arguments.get('pname',"")
        channel = self.arguments.get('channel',"")
        params = {}
        for key in ['ser', 'idfv', 'idfa', 'mac', 'rt', 'scopeid']:
            params[key] = self.arguments.get(key, "")
        fingerprinting = self.__get_devicefingerprinting(params)
        ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1 LIMIT 1", ip)
        cheat = 0
        cheatType = 0
        if ip_info:
            cheat = 1
            cheatType = 1
        idfa_info = self.db.get("SELECT * FROM `idfa_blacklist` WHERE `idfa` = %s AND `status`=1 LIMIT 1", params['idfa'])
        if idfa_info:
            cheat = 1
            cheatType = 3
        user_device = self.db.get(
            "SELECT `sid`, `fingerprinting` from `user_device` \
            where `fingerprinting` = %s",
            fingerprinting)
        if not user_device:
            # 新增一个设备id
            sid = self.db.execute_lastrowid(
                "INSERT INTO `user_device` (`idfa`, `idfv`, `mac`, `ser`,\
                `fingerprinting`, `ip`, `cheat`, `type`) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                params['idfa'], params['idfv'], params['mac'], params['ser'],fingerprinting,ip,int(cheat),int(cheatType))
        else:
            self.db.execute(
                "UPDATE `user_device` set `cheat` =  %s,\
                `ip` =  %s, \
                `idfa` = %s, \
                `type` = %s \
                WHERE `fingerprinting` = %s", cheat, ip, params['idfa'], cheatType, fingerprinting)
        self.return_result({
            "token": fingerprinting,
            "pname": pname,
            "channel": channel,
            })

    def __get_devicefingerprinting(self, device_params):
        """简单的生成设备指纹方法"""
        valid_params = [
            device_params['ser'],
            device_params['idfv'],
            device_params['idfa'],
            device_params['mac'],
        ]
        device_str = ':'.join(str(valid_params))
        return hashlib.md5(device_str).hexdigest()

class BindHandler(protocols.JSONBaseHandler):
    """用户登陆绑定"""
    @protocols.unpack_arguments_byscopeid(with_scopeid=False)
    def post(self):
        params = {}
        for key in ['scopeid', 'name', 'first_name', 'last_name', 'locale', 'gender', 'token']:
            params[key] = self.arguments.get(key, "")
        ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        params['platform'] = self.arguments.get('platform',"1")
        if self.first_login:
            # 更新用户信息
            self.fill_code=0
            invite_code=self.__get_invitecode(6)
            new_user=self.db.get("SELECT * FROM `options` WHERE `key`='new_user'")
            prize = int(new_user['values'])
            uid = self.db.execute_lastrowid(
            "INSERT INTO `user` (`scopeid`, `name`, `first_name`, `last_name`, `locale`, `gender`, `invited_code`, `points`,`total_points`, \
                `bind_points`,`token`,`last_login`, `platform`,`ip`)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )",
            params['scopeid'],params['name'], params['first_name'], params['last_name'], params['locale'],params['gender'], invite_code, \
                prize, prize, prize, params['token'],datetime.datetime.now(), params['platform'], ip)
            order="新用戶紅利"
            ad="新用戶紅利"
            self.db.execute(
                "INSERT INTO `callback_order`(`order`,`ad`,`user`,`platform`,`ad_source`,`points`)"
                "VALUES(%s,%s,%s,%s,%s,%s)", order,ad,uid,3,1,prize)
            self.db.execute(
                "INSERT INTO `global_orders` (uid, points, last, type, note)"
                "VALUES (%s, %s, %s, %s, %s)",
                uid, prize, 0, 1, ad)
            user_bind = self.db.get(
            "SELECT * FROM `user_bind` WHERE `userid`=%s AND `token`=%s LIMIT 1",
            params['scopeid'],params['token'])
            if not user_bind and params['token']!='':
                self.db.execute(
                    "INSERT INTO `user_bind` (`uid`, `userid`, `token`, `type`)"
                    "VALUES (%s, %s, %s, %s)",
                    uid, params['scopeid'], params['token'], 0)
            user_info=self.db.get(
            "SELECT * FROM `user` WHERE `scopeid` = %s", \
            params['scopeid'])
        else:
            user_info = self.db.get(
            "SELECT `uid`, `invited_code`, `bind_points`, `points`, `invited_by`,`like` from `user` \
            where `scopeid` = %s",
            params['scopeid'])
            self.db.execute(
                "UPDATE `user` set `token` =  %s,\
                `last_login` =  %s, \
                `ip` = %s, \
                `platform` = %s \
                WHERE `scopeid` = %s", params['token'], datetime.datetime.now(), ip, params['platform'], params['scopeid'])
            uid = user_info['uid']
            user_bind = self.db.get(
            "SELECT * FROM `user_bind` WHERE `userid`=%s AND `token`=%s LIMIT 1",
            params['scopeid'],params['token'])
            if not user_bind and params['token']!='':
                self.db.execute(
                    "INSERT INTO `user_bind` (`uid`, `userid`, `token`, `type`)"
                    "VALUES (%s, %s, %s, %s)",
                    user_info['uid'], params['scopeid'], params['token'], 0)

            if user_info['invited_by']==None:
                self.fill_code=0
            else:
                self.fill_code=1
        log_path = self.config['log']['bind_log']
        utils.print_log('bind', log_path, self.request.uri+"&Uid="+str(uid)+"&token="+str(params['token'])+"&IP="+str(ip))
        #print self.fill_code
        self.return_result({
        "uid": user_info['uid'],
        "scopeid": params['scopeid'],
        "points": user_info['points'],
        "bindScore": user_info['bind_points'],
        "invite" : user_info['invited_code'],
        "firs_login": self.first_login,
        "fill_code": self.fill_code,
        "is_fblike": user_info['like']
        })

    #生成邀请码
    def __get_invitecode(self, length):
        chars = string.ascii_letters+string.digits
        return ''.join([random.choice(chars) for i in range(length)])


class BindfbHandler(protocols.JSONBaseHandler):
    """用户facebook验证登陆绑定"""

    @protocols.unpack_arguments_byscopeid(with_scopeid=False)
    def post(self):
        params = {}
        for key in ['scopeid', 'name', 'first_name', 'last_name', 'locale', 'gender', 'token', 'access_token', 'email', \
                    'utm_campaign', 'utm_source', 'utm_medium', 'utm_content', 'utm_term']:
            params[key] = self.arguments.get(key, "")
        #print `params` + '-----------------------------params'
        params['platform'] = self.arguments.get('platform',"1")
        ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        fbValid = self.db.get("SELECT * FROM `options` WHERE `key` = 'fbValid'")
        if fbValid['values'] == 1:
            input_token = params['access_token']
            access_token = self.config['facebook']['access_token']
        #fburl = "https://graph.facebook.com/debug_token?input_token="+input_token+"&access_token="+access_token+""
            s = urllib2.urlopen("https://graph.facebook.com/debug_token?input_token="+input_token+"&access_token="+access_token+"")
        #t = requests.get(fburl, timeout=2)
        #print t+'t'
            r = json.load(s)
            if r['data']['user_id']!=params['scopeid'] or not r['data']['is_valid']:
                return
        else:
            print 'no fbValid'
        if self.first_login:
            # 更新用户信息
            self.fill_code=0
            invite_code=self.__get_invitecode(6)
            new_user=self.db.get("SELECT * FROM `options` WHERE `key`='new_user'")
            prize = int(new_user['values'])
            uid = self.db.execute_lastrowid(
            "INSERT INTO `user` (`scopeid`, `name`, `first_name`, `last_name`, `locale`, `gender`, `invited_code`, `points`,`total_points`, \
                `bind_points`,`token`,`last_login`, `platform`, `mail`,`ip`, `access_token`, \
                `utm_campaign`, `utm_source`, `utm_medium`, `utm_content`, `utm_term`)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                %s, %s, %s, %s, %s)",
            params['scopeid'],params['name'], params['first_name'], params['last_name'], params['locale'],params['gender'], invite_code, \
                prize, prize, prize, params['token'],datetime.datetime.now(), params['platform'], params['email'], ip, params['access_token'], \
                params['utm_campaign'], params['utm_source'], params['utm_medium'], params['utm_content'], params['utm_term'])
            if params['name'] == 'null':
                ip_blacklist = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip`=%s AND `status`=1 LIMIT 1",ip)
                if not ip_blacklist:
                    self.db.execute(
                        "INSERT INTO `ip_blacklist` (`ip`,`status`,`note`)" \
                        "VALUES (%s, %s, %s)", ip, 1, 'null name')
                user_blacklist = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid`=%s AND `status`=1 LIMIT 1", uid)
                if not user_blacklist:
                    self.db.execute(
                        "INSERT INTO `user_blacklist` (`uid`, `status`, `note`)" \
                        "VALUES (%s, %s, %s)", uid, 1, 'null name')
            order="新用戶紅利"
            ad="新用戶紅利"
            self.db.execute(
                "INSERT INTO `callback_order`(`order`,`ad`,`user`,`platform`,`ad_source`,`points`)"
                "VALUES(%s,%s,%s,%s,%s,%s)", order,ad,uid,3,1,prize)
            self.db.execute(
                "INSERT INTO `global_orders` (uid, points, last, type, note)"
                "VALUES (%s, %s, %s, %s, %s)",
                uid, prize, 0, 1, ad)
            user_bind = self.db.get(
            "SELECT * FROM `user_bind` WHERE `userid`=%s AND `token`=%s LIMIT 1",
            params['scopeid'],params['token'])
            if not user_bind and params['token']!='':
                self.db.execute(
                    "INSERT INTO `user_bind` (`uid`, `userid`, `token`, `type`)"
                    "VALUES (%s, %s, %s, %s)",
                    uid, params['scopeid'], params['token'], 0)

            user_info=self.db.get(
            "SELECT * FROM `user` WHERE `scopeid` = %s", \
            params['scopeid'])
        else:
            user_info = self.db.get(
            "SELECT `uid`, `invited_code`, `bind_points`, `points`, `invited_by`,`like` from `user` \
            where `scopeid` = %s",
            params['scopeid'])
            self.db.execute(
                "UPDATE `user` set `token` = %s,\
                `last_login` =  %s, \
                `mail` = %s, \
                `ip` = %s,\
                `access_token` = %s, \
                `platform` = %s \
                WHERE `scopeid` = %s", params['token'], datetime.datetime.now(), params['email'], ip, params['access_token'],params['platform'], params['scopeid'])
            uid = user_info['uid']
            if params['name'] == 'null':
                ip_blacklist = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip`=%s AND `status`=1 LIMIT 1",ip)
                if not ip_blacklist:
                    self.db.execute(
                        "INSERT INTO `ip_blacklist` (`ip`,`status`,`note`)" \
                        "VALUES (%s, %s, %s)", ip, 1, 'null name')
                user_blacklist = self.db.get("SELECT * FROM `user_blacklist` WHERE `uid`=%s AND `status`=1 LIMIT 1", uid)
                if not user_blacklist:
                    self.db.execute(
                        "INSERT INTO `user_blacklist` (`uid`, `status`, `note`)" \
                        "VALUES (%s, %s, %s)", uid, 1, 'null name')
            user_bind = self.db.get(
            "SELECT * FROM `user_bind` WHERE `userid`=%s AND `token`=%s AND `uid`=%s LIMIT 1",
            params['scopeid'], params['token'], uid)
            if (not user_bind) and (params['token']!=''):
                self.db.execute(
                    "INSERT INTO `user_bind` (`uid`, `userid`, `token`, `type`)"
                    "VALUES (%s, %s, %s, %s)",
                    user_info['uid'], params['scopeid'], params['token'], 0)

            if user_info['invited_by']==None:
                self.fill_code=0
            else:
                self.fill_code=1
        log_path = self.config['log']['bind_log']
        utils.print_log('bind', log_path, self.request.uri+"&Uid="+str(uid)+"&token="+str(params['token'])+"&IP"+str(ip))
        self.return_result({
        "uid": user_info['uid'],
        "scopeid": params['scopeid'],
        "points": user_info['points'],
        "bindScore": user_info['bind_points'],
        "invite" : user_info['invited_code'],
        "firs_login": self.first_login,
        "fill_code": self.fill_code,
        "is_fblike": user_info['like']
        })

    #生成邀请码
    def __get_invitecode(self, length):
        chars = string.ascii_letters+string.digits
        return ''.join([random.choice(chars) for i in range(length)])


class PointsHandler(protocols.JSONBaseHandler):
    """ 用户积分、等级、签到天数 """

    @protocols.unpack_arguments()
    def get(self):
        import urllib2
        params = {}
        params['token'] = self.arguments.get('token',"")
        params['scopeid'] = self.arguments.get('scopeid',"")
        params['idfa'] = self.arguments.get('idfa',"")
        params['language'] = self.arguments.get('language', 'zh')
        params['version'] = self.arguments.get('version', "")
        params['pname'] = self.arguments.get('pname', "")
        params['platform'] = self.arguments.get('platform', 1)
        params['imei'] = self.arguments.get('imei', "")
        params['mac'] = self.arguments.get('mac', "")
        params['android_id'] = self.arguments.get('android_id', "")
        adinfo = []
        adinfo1 = []
        adinfo_fyber = []
        params['advertising_id'] = self.arguments.get('advertising_id', '')
        ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        if not self.current_user:
            return
        # 统计英文版
        if params['language'] == 'en':
                self.db.execute(
                    "UPDATE `user` set `en`=1 WHERE `uid`=%s", self.current_user['uid'])
        # 有米ios推广
        if params['idfa'] != '':
            adinfo = self.db.get("SELECT * FROM `wallad_clicks` WHERE `status`=0 AND `create_time`>=(Curdate()-7) \
                                     AND `idfa`=%s LIMIT 1", params['idfa'])
            if adinfo:
                callback_url = adinfo['callback_url']
        # Tapjoy安卓推广
        if (params['advertising_id'] !='') and params['idfa'] == '':
            idfa = hashlib.new("sha1", params['advertising_id']).hexdigest()
            #print `idfa` + 'idfa'
            #AppId = 'd7e2de83-c0e6-4846-8c7b-4417e2edba40'
            AppId = 'acbb1fe2-18e6-434a-a300-3e3f42738885'
            adinfo1 = self.db.get("SELECT * FROM `wallad_clicks` WHERE `status`=0 AND `adserver`=2 \
                                 AND `create_time`>=(Curdate()-7) \
                                 AND `advertising_id`=%s LIMIT 1", idfa)
            if adinfo1:
                callback_url = 'https://ws.tapjoyads.com/log_device_app?app_id=%s&advertising_id=%s \
                    &sdk_type=connect&library_version=server'%(AppId,params['advertising_id'])
                callback_url = callback_url.replace(' ','')
                #print 'tj  ' + `callback_url` + 'callback_url'
        # fyber安卓推广
        if (params['imei'] !=''):
            fyber_points = self.db.get("SELECT `values` FROM `options` WHERE `key`='fyber_campaign_threshold'")
            appid='644cfd49af6d19ac415e662e59715b0b'
            #sha1_mac = hashlib.new("sha1", params['mac']).hexdigest()
            adinfo_fyber = self.db.get("SELECT * FROM `wallad_fyber` WHERE `status`=0 \
                                 AND `create_time`>=(Curdate()-7) \
                                 AND `device_id`=%s LIMIT 1", params['imei'])
            if adinfo_fyber:
                callback_url = 'http://service.sponsorpay.com/installs/v2?appid=%s&answer_received=0&ip=%s&device_id=%s&android_id=%s&mac_address=%s' \
                    %(appid, ip, params['imei'], params['android_id'], params['mac'])
                callback_url = callback_url.replace(' ','')
        # 有米安卓推广
        if params['idfa'] == '':
            adinfo = self.db.get("SELECT * FROM `wallad_clicks` WHERE `status`=0 AND `create_time`>=(Curdate()-7) \
                                 AND `token`=%s LIMIT 1", params['token'])
            if adinfo:
                callback_url = adinfo['callback_url']
        # 有米回调
        if adinfo:
            if self.current_user['points']>299:
                try:
                    msg = str(urllib2.urlopen(callback_url).read())
                except urllib2.HTTPError,e:
                    msg = str(e.code)
                except urllib2.URLError,e:
                    msg = str(e)
                self.db.execute(
                    "UPDATE `wallad_clicks` set `status`=1,`uid`=%s, `msg`=%s \
                    WHERE `id`=%s", self.current_user['uid'], msg, adinfo['id'])
        # tapjoy回调
        if adinfo1:
            if self.current_user['points']>299 and self.current_user['uid']>83000:
                try:
                    msg = str(urllib2.urlopen(callback_url).read())
                except urllib2.HTTPError,e:
                    msg = str(e.code)
                except urllib2.URLError,e:
                    msg = str(e)
                self.db.execute(
                    "UPDATE `wallad_clicks` set `status`=1,`uid`=%s, `msg`=%s, `callback_url`=%s \
                    WHERE `id`=%s", self.current_user['uid'], msg, callback_url, adinfo1['id'])
            else:
                self.db.execute(
                    "UPDATE `wallad_clicks` set `uid`=%s \
                    WHERE `advertising_id`=%s", self.current_user['uid'], idfa)
            # info = "idfa="+idfa+ "&advertising_id="+params['advertising_id']+"&scopeid="+params['scopeid']
            # log_path = self.config['log']['adifa_log']
            # utils.print_log('adifa', log_path, info)
            self.db.execute_lastrowid(
                "UPDATE `user` set `ad_from`=%s \
                WHERE `uid`=%s", 2, self.current_user['uid'])
        # fyber回调
        if adinfo_fyber:
            if self.current_user['points']>=fyber_points['values']:
                try:
                    msg = str(urllib2.urlopen(callback_url).read())
                except urllib2.HTTPError,e:
                    msg = str(e.code)
                except urllib2.URLError,e:
                    msg = str(e)
                self.db.execute(
                    "UPDATE `wallad_fyber` set `status`=1,`uid`=%s \
                    WHERE `id`=%s", self.current_user['uid'], adinfo_fyber['id'])
                self.db.execute_lastrowid(
                    "UPDATE `user` set `ad_from`=%s \
                    WHERE `uid`=%s", 3, self.current_user['uid'])
        if params['language'] == 'zh':
            en = 0
        else:
            en = 1
        self.db.execute(
            "UPDATE `user` set `ip` = %s, `last_login`=%s, `token`=%s , \
            `platform`=%s, `version`=%s, `en`=%s  \
            WHERE `scopeid` = %s", ip, datetime.datetime.now(), params['token'], params['platform'], \
            params['version'], en, params['scopeid'])
        black_ip=self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip`=%s AND `status`=1 LIMIT 1",ip)
        if black_ip:
            black_user=self.db.get("SELECT * FROM `user_blacklist` WHERE `uid`=%s AND `status`=1 LIMIT 1",self.current_user['uid'])
            if not black_user:
                msg='ip作弊'
                self.db.execute(
                    "INSERT INTO `user_blacklist` (`uid`, `note`)"
                    "VALUES (%s, %s)",
                    self.current_user['uid'], msg)
            self.db.execute(
                "UPDATE `user_device` set `cheat`=1, `type`=1 \
                WHERE `fingerprinting`=%s", params['token'])
        #  记录相关用户信息
        info = "uid=" + `int(self.current_user['uid'])` + "&version=" + `params['version']` + "&pname" + `params['pname']` + \
                "&platform=" + `params['platform']` + "&language=" + `params['language']` + \
                "&ip=" + `ip` + "&token=" + `params['token']` + "&scopeid=" + `params['scopeid']`
        log_path = self.config['log']['ip_log']
        utils.print_log('ip', log_path, info)
        ex_rate = self.db.get("SELECT * FROM `options` WHERE `key`='exchange_rate'")
        points = dict(
            points=self.current_user['points'],
            ex_points=self.current_user['ex_points'],
            ex_price=float(self.current_user['ex_points'])/float(ex_rate['values']),
            invite_points=self.current_user['invite_points'],
            total_points=self.current_user['total_points'],
            invite_num=self.current_user['invites'],
            alipay_account=self.current_user['alipay'],
        )
        self.return_result(points)


class PointsDetailHandler(protocols.JSONBaseHandler):
    """ 用户积分流水 """

    @protocols.unpack_arguments()
    def get(self):
        # d8iD0rnprIwYnYLHWACYciNejLEFTznTHP8B6+0VsoH90m15C7973Vywn
        # rkHJRrUNxAxgjDeswK5LLIR3208tpunHdqZWY6ce1mYYqPH/HA=
        orders = self.db.query(
            "SELECT * FROM `callback_order` WHERE `user` = %s ORDER BY `time` DESC",
            self.current_user['uid'])

        records = []
        for order in orders:
            records.append({
                'oid': order['id'],
                'type': order['ad_source'],
                'title':  order['ad'].encode('utf-8'),
                'score': order['points'],
                'create_time': order['time']})

        self.return_result({"records": records})



class SignInfoHandler(protocols.JSONBaseHandler):
    """ 用户签到时间查询 """

    @protocols.unpack_arguments()
    def get(self):
        signInfo = self.db.get(
            "SELECT * FROM `user_sign` WHERE `uid` = %s",
            self.current_user['uid'])
        log_path = self.config['log']['signinfo_log']
        day1 = self.db.get("SELECT * FROM `options` WHERE `key` = 'sign_prize1'")
        day2 = self.db.get("SELECT * FROM `options` WHERE `key` = 'sign_prize2'")
        day3 = self.db.get("SELECT * FROM `options` WHERE `key` = 'sign_prize3'")
        day4 = self.db.get("SELECT * FROM `options` WHERE `key` = 'sign_prize4'")
        day5 = self.db.get("SELECT * FROM `options` WHERE `key` = 'sign_prize5'")
        day6 = self.db.get("SELECT * FROM `options` WHERE `key` = 'sign_prize6'")
        sign_prize = 5
        if signInfo:
            times = signInfo['time']
            #print (datetime.datetime.now().date()-(times+datetime.timedelta(hours=8)).date()).days
            #print (datetime.datetime.now().date()-times.date()).days
            if 0<=(datetime.datetime.now().date()-times.date()).days<=1:
                #print times
                #print "days"
                int = (signInfo['day']+1)%6
                #print str(int)+"int"
                if int==2:
                    sign_prize=day2['values']
                if int==3:
                    sign_prize=day3['values']
                if int==4:
                    sign_prize=day4['values']
                if int==5:
                    sign_prize=day5['values']
                if int==6:
                    sign_prize=day6['values']
                if int==0:
                    sign_prize=day6['values']
            times = signInfo['time']-datetime.timedelta(hours=8)
        else:
            sign_prize=day1['values']
            times =0
            utils.print_log('signinfo', log_path, self.request.uri+"&lastSignTime:"+str(times)+"&user:"+str(self.current_user['uid'])+"&NextSignPoint:"+str(sign_prize))
        #print str(times)+"times"
        #timeArray = time.localtime(time.time())
        #otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        #print time.time()
        #print otherStyleTime
        taskInfo = self.db.get("SELECT * FROM `global_orders` WHERE `type`=6 AND `uid`=%s \
                               AND DATE_SUB(CURDATE(), INTERVAL 5 DAY) <= date(record_time) LIMIT 1", self.current_user['uid'])
        if taskInfo :
            showInterstitial = 0
            signable = True
        else:
            showInterstitial = 1
            signable = False
        self.return_result({
            "sign_time":times,
            "current_time":long(time.time()),
            "reward_points":sign_prize,
            "showInterstitial":showInterstitial,
            "signable":signable,
            #"user":self.current_user['uid'],
        })


class SignHandler(protocols.JSONBaseHandler):
    """ 用户签到 """

    @protocols.unpack_arguments()
    def get(self):
        ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s and `status`=1", ip)
        if ip_info:
            return
        day1 = self.db.get("SELECT * FROM `options` WHERE `key` = 'sign_prize1'")
        day2 = self.db.get("SELECT * FROM `options` WHERE `key` = 'sign_prize2'")
        day3 = self.db.get("SELECT * FROM `options` WHERE `key` = 'sign_prize3'")
        day4 = self.db.get("SELECT * FROM `options` WHERE `key` = 'sign_prize4'")
        day5 = self.db.get("SELECT * FROM `options` WHERE `key` = 'sign_prize5'")
        day6 = self.db.get("SELECT * FROM `options` WHERE `key` = 'sign_prize6'")
        order=ad="簽到"
        log_path = self.config['log']['sign_log']
        #timestamp = self.arguments.get('rt', "")
        #print timestamp
        timenow=int(time.time())
        now = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
        #sign_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timestamp)))
        sign_day = datetime.datetime.fromtimestamp(float(timenow))
        sign_day = sign_day.date()
        #print 'sign day'
        #print sign_day
        uid=self.db.get("SELECT `uid` FROM `user` WHERE `scopeid`=%s", self.arguments.get('scopeid',""))
        iuid = int(uid['uid'])
        # 检查用户当天是否已经签到
        #flag = self.db.get(
        #    "SELECT `id` FROM `user_sign` WHERE `uid`=%s AND DATE(`time`)=CURDATE()",
        #    uid['uid'])
        #fix me 十二点提示当天重复签到
        #if flag:
        #    self.return_error(constants.ERR_REPEAT_SIGN)
        #    return
        #连续签到天数
        signInfo=self.db.get("SELECT * FROM `user_sign` WHERE `uid`=%s",
                             self.current_user['uid'])
        if signInfo:
            #print 'signTime'
            signInfo['time']=signInfo['time']
            #print signInfo['time']
            signInfo['time']=signInfo['time'].date()
            diff = (sign_day-signInfo['time']).days
            #print signInfo['time']
            #print 'diff'+str(diff)
            #print (sign_day-signInfo['time']).days
            #if (((sign_day-signInfo['time'])).days==1) and (not flag):
            if (((sign_day-signInfo['time'])).days==1):
            #if (((sign_day-signInfo['time']))<=datetime.timedelta(days=2)) and (not flag):
                if signInfo['day']==1:
                    self.saveSign(iuid,order,ad,self.current_user['scopeid'],day2['values'],4,2,1,day2['values'],now)
                if signInfo['day']==2:
                    self.saveSign(iuid,order,ad,self.current_user['scopeid'],day3['values'],4,3,1,day3['values'],now)
                if signInfo['day']==3:
                    self.saveSign(iuid,order,ad,self.current_user['scopeid'],day4['values'],4,4,1,day4['values'],now)
                if signInfo['day']==4:
                    self.saveSign(iuid,order,ad,self.current_user['scopeid'],day5['values'],4,5,1,day5['values'],now)
                if signInfo['day']==5:
                    self.saveSign(iuid,order,ad,self.current_user['scopeid'],day6['values'],4,6,1,day6['values'],now)
                if signInfo['day']==6:
                    self.saveSign(iuid,order,ad,self.current_user['scopeid'],day1['values'],4,1,1,day1['values'],now)
            #elif (sign_day-signInfo['time']).days!=1 and (not flag) and (sign_day-signInfo['time']).days!=0:
            elif (sign_day-signInfo['time']).days!=1 and (sign_day-signInfo['time']).days!=0:
                if signInfo['status']==0:
                    self.saveSign(iuid,order,ad,self.current_user['scopeid'],day1['values'],4,1,1,day1['values'],now)
                if signInfo['status']==1:
                    self.saveSign(iuid,order,ad,self.current_user['scopeid'],day1['values'],4,1,0,day1['values'],now)
            elif ((sign_day-signInfo['time']).days==0):
                self.return_error(constants.ERR_REPEAT_SIGN)
                return

        else:
            self.db.execute(
                "INSERT INTO `user_sign` (uid,time,appType)"
                "VALUES (%s, %s, 0)",iuid, str(now))
            self.saveSign(iuid,order,ad,self.current_user['scopeid'],day1['values'],4,1,1,day1['values'],now)
            diff = 0
        utils.print_log('sign', log_path, self.request.uri+"&SignTime:"+str(now)+"&user:"+str(self.current_user['uid'])+"&diff:"+str(diff))

    def saveSign(
            self, order,ad,uid, scopeid, points,
            ad_source, day, status, sign_prize, now):
        iuid = int(self.current_user['uid'])
        self.db.execute(
            "UPDATE `user_sign` set `day`=%s, `status`=%s, `time`=%s WHERE `uid`=%s", day, status, now, iuid)
        oid=self.db.execute_lastrowid(
            "INSERT INTO `global_orders` (uid, points, last, type, note)"
            "VALUES (%s, %s, %s, %s, %s)",
            iuid, sign_prize, self.current_user['points'], 4, ad)

        self.db.execute(
            'INSERT INTO  `callback_order` (`order`, `oid`, `ad`,\
            `user`, `points`, `platform`, `ad_source`) '
            "VALUES (%s, %s, %s, %s, %s,  3, 4)",
            order, oid, ad, iuid, points)
        self.db.execute(
            "UPDATE `user` set `points` = `points` + %s,\
            `total_points` = `total_points` + %s, `sign_days` =`sign_days`+1\
            WHERE `uid` = %s", sign_prize, sign_prize, iuid)

        timenow=int(time.time())
        #print 'timenow'
        #print timenow

        self.return_result({
            "points":self.current_user['points'],
            "days":day,
            "times":timenow,
            "getPoint":sign_prize,
        })


class LevelHandler(protocols.JSONBaseHandler):
    """ 等级奖励信息 """

    @protocols.unpack_arguments()# 解密s参数
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
            self.current_user['uid'], level)
        if flag:
            self.return_error(constants.ERR_REPEAT_AWARD)
            return

        level_prize = self.db.get(
            "SELECT * FROM `level_prize`"
            "WHERE `level` = %s", level)
        self.db.execute(
            "UPDATE `user` SET `points` = `points` + %s, `total_points` = `total_points` + %s"
            "WHERE `uid` = %s", level_prize['prize'], level_prize['prize'], self.current_user['uid'])
        self.db.execute(
            "INSERT INTO `level_prize_re`(`uid`, `level`, `prize`)"
            "VALUES(%s, %s, %s)", self.current_user['uid'], level, level_prize['prize'])
        self.return_success()


class TodayHandler(protocols.JSONBaseHandler):
    """ 用户每日推荐 """

    @protocols.unpack_arguments()
    def get(self):
        uid = self.current_user['uid']
        # 每日推荐信息
        daily = self.db.query(
            "SELECT * FROM `daily_reward` WHERE `status`=1 ")
        ad = "每日獎勵"
        records = []
        for d in daily:
        # 任务收益
            if d['ad_id'] != 1000:
                complete_count = self.db.get(
                    "SELECT count(*) FROM `callback_order` "
                    "WHERE `user` = %s AND DATE(`time`) = CURDATE() AND `ad_source` = %s", uid,d['ad_id'])
            else:
                complete_count = self.db.get(
                    "SELECT count(*) FROM `callback_order` "
                    "WHERE `user` = %s AND DATE(`time`) = CURDATE() AND `ad_source` >= 100 AND `points`>9", uid)
            if complete_count['count(*)'] >= d['total_task']:
                task = self.db.get(
                    "SELECT `id` FROM `global_orders` "
                    "WHERE `type` = 12 AND DATE(`record_time`) = CURDATE() AND `note`= %s AND `uid`= %s LIMIT 1", \
                    d['ad_id'], self.current_user['uid'])
                if not task:
                    oid=self.db.execute_lastrowid(
                        "INSERT INTO `global_orders` (uid, points, last, type, note)"
                        "VALUES (%s, %s, %s, %s, %s)",
                        uid, d['points'], self.current_user['points'], 12, d['ad_id'])
                    self.db.execute(
                        'INSERT INTO  `callback_order` (`order`, `oid`, `ad`,\
                        `user`, `points`, `platform`, `ad_source`) '
                        "VALUES (%s, %s, %s, %s, %s,  3, 12)",
                        ad, oid, ad, uid, d['points'])
                    self.db.execute(
                        "UPDATE `user` set `points` = `points` + %s, `total_points` = `total_points` + %s \
                        WHERE `uid` = %s", d['points'], d['points'], self.current_user['uid'])
            records.append({
                'adplatform': d['ad_id'],
                'title': d['title'].encode('utf-8'),
                'description':  d['description'].encode('utf-8'),
                'total_count': d['total_task'],
                'complete_count': complete_count['count(*)'],
                'point': d['points']})

        self.return_result({"lists": records})


class NewUserHandler(protocols.JSONBaseHandler):
    """ 新手推荐 """

    @protocols.unpack_arguments()
    def get(self):
        task = self.db.get(
            "SELECT `id` FROM `global_orders` "
            "WHERE `type` = 6 AND `uid`= %s LIMIT 1", self.current_user['uid'])
        if task:
            ftask = 1
        else:
            ftask = 0
        exchange = self.db.get(
            "SELECT `id` FROM `global_orders` "
            "WHERE `type` = 5 AND `uid`= %s LIMIT 1", self.current_user['uid'])
        if exchange:
            fexchange = 1
        else:
            fexchange = 0

        if self.current_user['invited_by'] != None:
            Fill_invite = 1
        else:
            Fill_invite = 0
        self.return_result({
            "Fill_invite":Fill_invite,
            "facebook_like":self.current_user['like'],
            "invite_friend":self.current_user['invites'],
            "first_task":ftask,
            "first_exchange":fexchange,})


class OthExchangeHandler(protocols.JSONBaseHandler):
    """ 其他用户兑换列表 """

    @protocols.unpack_arguments(with_scopeid=False)
    def get(self):
        # 每日推荐信息
        othExchange = self.db.query(
            "SELECT `uid`,`create_time`,`goods_title` FROM `exchange_orders` \
            WHERE `status`=1 ORDER BY `create_time` DESC LIMIT 20")
        records = []
        for o in othExchange:
            user = self.db.get(
            "SELECT `name` FROM `user` "
            "WHERE `uid`= %s LIMIT 1", o['uid'])
            uname = ''
            if user:
                name = user['name']
                sname = list(name)
                uname = sname[0]+'***'+sname[-1]
            # 任务收益
            records.append({
                'user_name': uname,
                'ex_title': o['goods_title'].encode('utf-8'),
                'ex_time':  o['create_time'],
            })
        self.return_result({"current_time":long(time.time()),"ex_list": records})

