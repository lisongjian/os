#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

配置模块

@author zhenyong

"""

import protocols
import constants
import time


class AdConfigHandler(protocols.JSONBaseHandler):
    """ 广告配置 """

    @protocols.unpack_arguments()
    def get(self):
        all_config = self.db.query(
            "SELECT `ad_id`, `title`, `intro`, `detail`, `credits`, `icon`, `aos_status`, "
            "`ios_status`, `priority` FROM `ad_config`")
        user_device = self.db.get(
            "SELECT `platform` FROM `user_device` WHERE `uid` = %s",
            self.current_user['uid'])

        configs = []
        for config in all_config:
            if (3 == user_device['platform'] and
                1 == config['aos_status']) or \
                (5 == user_device['platform'] and
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


class TaskHandler(protocols.JSONBaseHandler):
    """ 今日推荐 """

    @protocols.unpack_arguments()
    def get(self):
        task = self.db.get("SELECT * FROM `options` WHERE `key` = 'task_id'")
        self.return_result({"task_id": task['values']})


class ChangelogHandler(protocols.JSONBaseHandler):
    """ 版本更新检查 """

    @protocols.unpack_arguments()
    def get(self):
        # platform: 平台号； distribute_kind: 渠道号
        type_id = self.arguments.get('platform')
        distribute_id = self.arguments.get('distribute_kind')

        if not type_id.isdigit() or not distribute_id.isdigit():
            self.return_error(constants.ERR_PROTOCOL_ERROR)

        type_id = int(type_id)
        distribute_id = int(distribute_id)

        latest = self.db.get(
            "SELECT `release_time`, `version`, `version_number`, `changelog`, `download_url` "
            "FROM `changelogs` WHERE `platform` = %s AND `distribute_kind` = %s "
            "ORDER BY `release_time` DESC LIMIT 1", type_id, distribute_id)

        if not latest:
            latest = {}
        else:
            latest['release_time'] = time.mktime(latest['release_time'].timetuple())

        self.return_result({"latest": latest})
