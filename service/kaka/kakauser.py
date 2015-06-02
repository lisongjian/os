#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

用户相关
@author zhenyong, lisongjian@youmi.net

"""

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
        ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s AND `status`=1", ip)
        cheat = 0
        cheatType = 0
        if ip_info:
            cheat = 1
            cheatType = 1
        imei_info = self.db.get("SELECT * FROM `imei_blacklist` WHERE `imei` = %s AND `status`=1", params['ei'])
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

        self.return_result({
            "token": fingerprinting,
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
        ip_info = self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip` = %s", ip)
        if ip_info:
            cheat = 1
            cheatType = 1
        idfa_info = self.db.get("SELECT * FROM `idfa_blacklist` WHERE `idfa` = %s", params['idfa'])
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
                `fingerprinting`, `ip`, `chaet`, `type`) "
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


class BindfbHandler(protocols.JSONBaseHandler):
    """用户facebook验证登陆绑定"""

    @protocols.unpack_kakaarguments_byscopeid(with_scopeid=False)
    def post(self):
        params = {}
        for key in ['scopeid', 'name', 'first_name', 'last_name', 'locale', 'gender', 'token', 'access_token', 'email', \
                    'utm_campaign', 'utm_source', 'utm_medium', 'utm_content', 'utm_term']:
            params[key] = self.arguments.get(key, "")
        params['platform'] = self.arguments.get('platform',"1")
        ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        fbValid = self.db.get("SELECT * FROM `options` WHERE `key` = 'fbValid'")
        if fbValid['values'] == 1:
            input_token = params['access_token']
            access_token = self.config['kakafb']['kaka_token']
            s = urllib2.urlopen("https://graph.facebook.com/debug_token?input_token="+input_token+"&access_token="+access_token+"")
            r = json.load(s)
            if r['data']['user_id']!=params['scopeid'] or not r['data']['is_valid']:
                return
                # print 'not fb'
        else:
            # print 'no fbValid'
            pass
        if self.first_login:
            # 更新用户信息
            self.fill_code=0
            invite_code=self.__get_invitecode(6)
            new_user=self.db.get("SELECT * FROM `options` WHERE `key`='new_user'")
            prize = int(new_user['values'])
            uid = self.db.execute_lastrowid(
            "INSERT INTO `user` (`scopeid`, `name`, `first_name`, `last_name`, `locale`, `gender`, `invited_code`, `points`,`total_points`, \
                `bind_points`,`token`,`last_login`, `platform`, `mail`,`ip`,`appType`, \
                `utm_campaign`, `utm_source`, `utm_medium`, `utm_content`, `utm_term`)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , \
                %s, %s, %s, %s, %s)",
            params['scopeid'],params['name'], params['first_name'], params['last_name'], params['locale'],params['gender'], invite_code, \
                prize, prize, prize, params['token'],datetime.datetime.now(), params['platform'], params['email'], ip, 1, \
                params['utm_campaign'], params['utm_source'], params['utm_medium'], params['utm_content'], params['utm_term'])
            order="新用戶紅利"
            ad="新用戶紅利"
            self.db.execute(
                "INSERT INTO `callback_order`(`order`,`ad`,`user`,`platform`,`ad_source`,`points`,`appType`)"
                "VALUES(%s,%s,%s,%s,%s,%s,%s)", order,ad,uid,3,1,prize,1)
            self.db.execute(
                "INSERT INTO `global_orders` (uid, points, last, type, note, appType)"
                "VALUES (%s, %s, %s, %s, %s, %s)",
                uid, prize, 0, 1, ad, 1)
            user_bind = self.db.get(
            "SELECT * FROM `user_bind` WHERE `userid`=%s AND `token`=%s LIMIT 1",
            params['scopeid'],params['token'])
            if not user_bind and params['token']!='':
                self.db.execute(
                    "INSERT INTO `user_bind` (`uid`, `userid`, `token`, `type`)"
                    "VALUES (%s, %s, %s, %s)",
                    uid, params['scopeid'], params['token'], 0)

            user_info=self.db.get(
            "SELECT * FROM `user` WHERE `scopeid` = %s AND `appType`=1", \
            params['scopeid'])
        else:
            user_info = self.db.get(
            "SELECT `uid`, `invited_code`, `bind_points`, `points`, `invited_by`,`like` from `user` \
            where `scopeid` = %s AND `appType`=1",
            params['scopeid'])
            self.db.execute(
                "UPDATE `user` set `token` = %s,\
                `last_login` =  %s, \
                `mail` = %s, \
                `ip` = %s,\
                `platform` = %s \
                WHERE `scopeid` = %s", params['token'], datetime.datetime.now(), params['email'], ip, params['platform'], params['scopeid'])
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
        utils.print_log('bind', log_path, self.request.uri+"kaka&Uid="+str(uid)+"&token="+str(params['token'])+"&IP"+str(ip)+"&appType=kaka")
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

    @protocols.unpack_kakaarguments_byscopeid()
    def get(self):
        import urllib2
        params = {}
        params['token'] = self.arguments.get('token',"")
        params['scopeid'] = self.arguments.get('scopeid',"")
        adinfo = self.db.get("SELECT * FROM `wallad_clicks` WHERE `status`=-1 AND `create_time`>=(Curdate()-7) \
                             AND `token`=%s AND `appType`=1 LIMIT 1", params['token'])
        if adinfo:
            if self.current_user['points']>299:
                try:
                    msg = str(urllib2.urlopen(adinfo['callback_url']).read())
                except urllib2.HTTPError,e:
                    msg = str(e.code)
                except urllib2.URLError,e:
                    msg = str(e)
                self.db.execute(
                    "UPDATE `wallad_clicks` set `status`=1,`uid`=%s, `msg`=%s \
                    WHERE `id`=%s AND `appType`=1", self.current_user['uid'], msg, adinfo['id'])
        ip = str( self.request.headers.get('X-Real-Ip', None)).split(',')[0]
        self.db.execute(
            "UPDATE `user` set `ip` = %s ,`last_login`=%s, `token`=%s\
            WHERE `scopeid` = %s AND `appType`=1", ip, datetime.datetime.now(), params['token'], params['scopeid'])
        black_ip=self.db.get("SELECT * FROM `ip_blacklist` WHERE `ip`=%s AND `status`=1",ip)
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
        info = "ip="+ip+ "kaka&token="+params['token']+"&scopeid="+params['scopeid']
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

    @protocols.unpack_kakaarguments_byscopeid()
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

    @protocols.unpack_kakaarguments_byscopeid()
    def get(self):
        signInfo = self.db.get(
            "SELECT * FROM `user_sign` WHERE `uid` = %s and `appType`=1 LIMIT 1",
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
            utils.print_log('signinfo', log_path, self.request.uri+"kaka&lastSignTime:"+str(times)+"&user:"+str(self.current_user['uid'])+"&NextSignPoint:"+str(sign_prize))
        # print str(times)+"times"
        # timeArray = time.localtime(time.time())
        # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        #print time.time()
        #print otherStyleTime
        self.return_result({
            "sign_time":times,
            "current_time":long(time.time()),
            "reward_points":sign_prize,
            #"user":self.current_user['uid'],
        })


class SignHandler(protocols.JSONBaseHandler):
    """ 用户签到 """

    @protocols.unpack_kakaarguments_byscopeid()
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
        #print now+'now'
        #sign_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timestamp)))
        sign_day = datetime.datetime.fromtimestamp(float(timenow))
        #print 'sign_day'+str(sign_day)
        sign_day = sign_day.date()
        #print 'sign day'
        #print sign_day
        uid=self.db.get("SELECT `uid` FROM `user` WHERE `scopeid`=%s and `appType`=1", self.arguments.get('scopeid',""))
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
        signInfo=self.db.get("SELECT * FROM `user_sign` WHERE `uid`=%s and `appType`=1 LIMIT 1",
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
                "VALUES (%s, %s, 1)",iuid, str(now))
            self.saveSign(iuid,order,ad,self.current_user['scopeid'],day1['values'],4,1,1,day1['values'],now)
            diff = 0
        utils.print_log('sign', log_path, self.request.uri+"kaka&SignTime:"+str(now)+"&user:"+str(self.current_user['uid'])+"&diff:"+str(diff))

    def saveSign(
            self, order,ad,uid, scopeid, points,
            ad_source, day, status, sign_prize, now):
        iuid = int(self.current_user['uid'])
        self.db.execute(
            "UPDATE `user_sign` set `day`=%s, `status`=%s, `time`=%s,`appType`=1 WHERE `uid`=%s", day, status, now, iuid)
        oid=self.db.execute_lastrowid(
            "INSERT INTO `global_orders` (uid, points, last, type, note, appType)"
            "VALUES (%s, %s, %s, %s, %s,%s)",
            iuid, sign_prize, self.current_user['points'], 4, ad, 1)

        self.db.execute(
            'INSERT INTO  `callback_order` (`order`, `oid`, `ad`,\
            `user`, `points`, `platform`, `ad_source`, `appType`) '
            "VALUES (%s, %s, %s, %s, %s,  3, 4, 1)",
            order, oid, ad, iuid, points)
        self.db.execute(
            "UPDATE `user` set `points` = `points` + %s,\
            `total_points` = `total_points` + %s, `sign_days` =`sign_days`+1\
            WHERE `uid` = %s AND `appType`=1", sign_prize, sign_prize, iuid)

        timenow=int(time.time())
        #print 'timenow'
        #print timenow

        self.return_result({
            "points":self.current_user['points'],
            "days":day,
            "times":timenow,
            "getPoint":sign_prize,
        })



