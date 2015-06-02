#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

配置模块

@author zhenyong

"""

import tornado.escape
import tornado.web
import protocols
import constants
import time,datetime
import json,httplib


class AdConfigHandler(protocols.JSONBaseHandler):
    """ 广告配置 """

    @protocols.unpack_arguments(with_scopeid=False)
    def get(self):
        user_device=self.arguments.get('device',"")
        pname = self.arguments.get('pname', "")
        days = int(self.arguments.get('days', 1))
        version = int(self.arguments.get('version', 1))
        all_config = self.db.query(
            "SELECT * FROM `ad_config` WHERE `appType`=0 ORDER BY `priority`")
        googleAudit = self.db.get("SELECT * from `options` WHERE `key` = 'googleAudit'")
        # aos低版本屏蔽adxmi积分墙
        if version<38 and user_device=="3":
            all_config = self.db.query(
            "SELECT * FROM `ad_config` WHERE `appType`=0 and `ad_id`!=119 ORDER BY `priority`")
            # 谷歌审核屏蔽
            if googleAudit['values']==1 and days<1:
                all_config = self.db.query(
                "SELECT * FROM `ad_config` WHERE `appType`=0 and `ad_id`!=107 and `ad_id`!=117 and`ad_id`!=119 ORDER BY `priority`")
        # 谷歌审核屏蔽
        if googleAudit['values']==1 and days<1:
            all_config = self.db.query(
            "SELECT * FROM `ad_config` WHERE `appType`=0 and `ad_id`!=107 and `ad_id`!=117  ORDER BY `priority`")
        configs = []
        for config in all_config:
            if (("3" == user_device )and
                (1 == config['aos_status']) and \
                (config['pname'] != pname) ) or \
                ("5" == user_device and
                1 == config['ios_status']) and \
                (config['channel'] != 3):
                configs.append({
                    "cfid": config['ad_id'],
                    "icon": config['icon'],
                    "title": config['title'],
                    "intro": config['intro'],
                    "detail": config['detail'],
                    "credits": config['credits'],
                    "priority": config['priority'],
                    "status": 1
                })

        self.return_result({"configs": configs})


class AnnounceHandler(protocols.JSONBaseHandler):
    """ 公告列表 """

    @protocols.unpack_arguments(with_scopeid=False)
    def get(self):
        #platform = self.arguments.get('platform')
        query = int(self.arguments.get('query'))
        page = int(self.arguments.get('page'))
        language = self.arguments.get('language', 'zh')
        if language == 'zh':
            time = self.db.get("SELECT max(id),`time` FROM `announce` \
                               WHERE `language`=0")
        elif language != 'zh':
            time = self.db.get("SELECT max(id),`time` FROM `announce` \
                               WHERE `language`=1")
        if query == 1:
            self.return_result({"time": time['time']})
        elif query == 0:
            info =0
            all_announce = []
            if language == 'zh':
                all_announce = self.db.query(
                    "SELECT `id`, `title`, `content`, `url`, `time`, `enddate`" \
                    "FROM `announce` WHERE `language`=0 ORDER BY `time` DESC LIMIT %s, %s",
                    page*20, (page+1)*20)
                info = self.db.execute_rowcount("SELECT `id` FROM `announce` WHERE `language`=0")
            elif language != 'zh':
                all_announce = self.db.query(
                    "SELECT `id`, `title`, `content`, `url`, `time`, `enddate`" \
                    "FROM `announce` WHERE `language`=1 ORDER BY `time` DESC LIMIT %s, %s",
                    page*20, (page+1)*20)
                info = self.db.execute_rowcount("SELECT `id` FROM `announce` WHERE `language`=1")
            if (info-(page+1)*20)>=0:
                nomore = 0
            else:
                nomore = 1
            Aannounces = []
            Fannounces = []
            for announce in all_announce:
                today = datetime.date.today()
                if announce['enddate'] > today:
                    active=True
                    Aannounces.append({
                        "title": announce['title'],
                        "content": announce['content'],
                        "atime": announce['time'],
                        "url": announce['url'],
                        "active": active,
                    })
                else:
                    active=False
                    Fannounces.append({
                    "title": announce['title'],
                    "content": announce['content'],
                    "atime": announce['time'],
                    "url": announce['url'],
                    "active": active,
                })
            for v in Fannounces:
               Aannounces.append(v)
            self.return_result({"time":time['time'], "nomore":nomore, "announces": Aannounces})


class ChangelogHandler(protocols.JSONBaseHandler):
    """ 版本更新检查 """

    @protocols.unpack_arguments(with_scopeid=False)
    def get(self):
        # distribute_kind: 渠道号
        distribute_id = self.arguments.get('distribute_kind')
        if not distribute_id.isdigit():
            self.return_error(constants.ERR_PROTOCOL_ERROR)

        distribute_id = int(distribute_id)

        latest = self.db.get(
            "SELECT `release_time`, `version`, `version_number`, `changelog`, `download_url` "
            "FROM `changelogs` WHERE `distribute_kind` = %s AND `appType`=0 "
            "ORDER BY `release_time` DESC LIMIT 1", distribute_id)

        if not latest:
            latest = {}
        else:
            latest['release_time'] = time.mktime(latest['release_time'].timetuple())

        self.return_result({"latest": latest})

    def push(self):
        """推送到Parse"""
        connection = httplib.HTTPSConnection('api.parse.com', 443)
        connection.connect()
        connection.request('POST', '/1/push', json.dumps({
            "where": {
                 "deviceType": "android",
            },
            "data": {
                 "action": 3,
                 "alert": "發現新版本"
            }
            }), {
            "X-Parse-Application-Id": self.config['push']['ApplicationId'],
            "X-Parse-REST-API-Key": self.config['push']['APIKey'],
            "Content-Type": "application/json"
             })

class PopularizeHandler(protocols.JSONBaseHandler):
    """ 公告列表 """

    @protocols.unpack_arguments(with_scopeid=False)
    def get(self):
        #platform = self.arguments.get('platform')
        all_popularize = self.db.query(
            "SELECT * FROM `popularize` WHERE `status`=1 ORDER BY `id` DESC ")
        popularizes = []
        for popularize in all_popularize:
            popularizes.append({
                "package": popularize['pname'],
                "title": popularize['title'],
                "content": popularize['content'],
                "icon": "http://www.gofree.hk/popularize/"+popularize['icon'],
                "url": popularize['url'],
            })
        self.return_result({"apps": popularizes})

class LoadpageHandler(protocols.JSONBaseHandler):
    """ 启动广告 """

    @protocols.unpack_arguments(with_scopeid=False)
    def get(self):
        platform = self.arguments.get('platform',1)
        language = self.arguments.get('language','zh')
        density = self.arguments.get('density','')
        loadpage = self.db.get(
            "SELECT * FROM `loadpage` WHERE `platform`=%s AND `density`=%s AND `lang`=%s ORDER BY `id` DESC \
            LIMIT 1",platform, density, language)
        if not loadpage:
            self.write('no loadpage')
            return
        d = {
                "image_url": loadpage['image_url'],
                #"icon": "http://www.gofree.hk/popularize/"+popularize['icon'],
                "ad_address": loadpage['ad_address'],
            }
        self.return_result(d)

class MissionHandler(protocols.JSONBaseHandler):
    """ 红利自有任务列表 """

    @protocols.unpack_arguments(with_scopeid=True)
    def get(self):
        #platform = self.arguments.get('platform')
        base_url = self.config['url']['base']
        all_mission = self.db.query(
            "SELECT * FROM `mission` WHERE `status`=1 AND `stime`<(curdate()) ORDER BY `id` DESC ")
        Amissions = []
        time_limit = False
        number_limit = False
        today =datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        for mission in all_mission:
            id=int(mission['id'])
            count = self.db.get("SELECT COUNT(*) FROM `go_mission` WHERE `mission_id`= %s AND \
                                `stime` BETWEEN %s and %s", id, today, tomorrow)
            rest = int(mission['limit']) - int(count['COUNT(*)'])
            if mission['etime'] > datetime.datetime.now():
                if mission['time_limit'] == 1:
                    time_limit = True
                if mission['number_limit'] == 1:
                    number_limit = True
                Amissions.append({
                    "icon": mission['icon'],
                    "title": mission['title'],
                    "description": mission['description'],
                    "point": mission['point'],
                    "time_limit": time_limit,
                    "number_limit": number_limit,
                    "rest": rest,
                    "url": base_url+"v1/gomission/"+`int(mission['id'])`+"/webpage",
                })
        self.return_result({"list":Amissions})


class GomissionHandler(protocols.JSONBaseHandler):
    """ 跳转任务 """

    @protocols.unpack_arguments(with_scopeid=False)
    def get(self, id):
        scopeid = self.arguments.get("scopeid",'')
        data=self.db.get("SELECT * FROM `mission` WHERE `id`=%s", id)
        self.render("task.html", data=data, scopeid=scopeid)

    def post(self, id):
        params = {}
        params['lineId'] = ''
        params['scopeid'] = ''
        data=self.db.get("SELECT * FROM `mission` WHERE `id`=%s", id)
        for key in ['email', 'lineId', 'scopeid']:
            v = self.get_argument(key, '')
            params[key] = tornado.escape.xhtml_escape(v) if v else params[key]
        if data['rest'] >0 :
            uid = self.db.get("SELECT `uid`, `invited_code` FROM `user` WHERE `scopeid`=%s", params['scopeid'])
            info = self.db.get("SELECT * FROM `go_mission` WHERE `uid`=%s AND `mission_id`=%s LIMIT 1", uid['uid'], id)
            today = datetime.datetime.now().date()
            tomorrow = today + datetime.timedelta(days=1)
            count = self.db.get("SELECT COUNT(*) FROM `go_mission` WHERE `mission_id`= %s AND \
                                `stime` BETWEEN %s and %s",id, today, tomorrow)
            if int(count['COUNT(*)']) >= data['limit']:
                self.write_json({"value":0})
                return
            if info:
                self.write_json({"value":2})
                return
            self.write_json({"value":2})
            self.db.execute("UPDATE `mission` set `rest`=`rest`-1 WHERE `id`=%s", id)
            self.db.execute("INSERT INTO `go_mission` (uid, email, lineID, mission_id, stime, iv_code)"
                            "VALUE (%s, %s, %s, %s, %s, %s)",
                            uid['uid'], params['email'], params['lineId'], id, datetime.datetime.now(), uid['invited_code'])
        if data['rest'] == 0 :
            self.write_json({"value":0})

    def write_json(self, response=None):
        self.set_header('Content-type', 'application/json; charset=UTF-8')
        self.write(json.dumps(response))

