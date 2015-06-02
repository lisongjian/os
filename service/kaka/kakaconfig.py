#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

配置模块

@author zhenyong

"""

import protocols
import constants
import time
import json,httplib



class AdConfigHandler(protocols.JSONBaseHandler):
    """ 广告配置 """

    @protocols.unpack_arguments(with_scopeid=False)
    def get(self):
        user_device=self.arguments.get('device',"")
        all_config = self.db.query(
            "SELECT `ad_id`, `title`, `intro`, `detail`, `credits`, `icon`, `aos_status`, "
            "`ios_status`, `priority`, `description` FROM `ad_config` ORDER BY `priority`")

        configs = []
        for config in all_config:
            if ("3" == user_device and
                1 == config['aos_status']) or \
                ("5" == user_device and
                 1 == config['ios_status']):
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
            "FROM `changelogs` WHERE `distribute_kind` = %s AND `appType`=1 "
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
            "X-Parse-Application-Id": self.config['kakapush']['ApplicationId'],
            "X-Parse-REST-API-Key": self.config['kakapush']['APIKey'],
            "Content-Type": "application/json"
             })
