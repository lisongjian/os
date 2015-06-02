#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author chenjiehua@youmi.net
#

""" 邀请相关 """

import protocols
import constants


class TopHandler(protocols.JSONBaseHandler):
    """ 邀请人排行榜 """

    @protocols.unpack_arguments()
    def get(self):
        top = self.db.query(
            "SELECT `uid`, `grade`, `invites` FROM `user` "
            "WHERE `invites`>0 ORDER BY `invites` DESC LIMIT 20")

        self.return_result({"top": top})


class DownloadHandler(protocols.JSONBaseHandler):
    """ 下载链接跳转 """

    @protocols.unpack_arguments()
    def get(self):
        platform = self.arguments.get('platform')
        download = self.db.get(
            "SELECT `download_url` FROM `changelogs` "
            "WHERE `platform` = %s ORDER BY `release_time` "
            "DESC LIMIT 1", platform)

        if not download:
            self.write("出错啦～～～")
            return

        self.db.execute(
            "INSERT INTO `invite_re`(`uid`, `ip`)"
            "VALUES(%s, %s)", self.current_user['id'], self.request.remote_ip)
        self.redirect(download['download_url'])


class CheckInviteHandler(protocols.JSONBaseHandler):
    """ 检查该用户是否为 被邀请 """

    @protocols.unpack_arguments()
    def get(self):
        ip = self.arguments.get('ip')
        rt = self.arguments.get('rt')
        invite = self.db.get(
            "SELECT `id`, `uid`, `time` FROM `invite_re` "
            "WHERE `ip` = %s AND `used` = 0 "
            "ORDER BY `time` DESC LIMIT 1", ip)
        # 无人邀请该用户
        if not invite:
            self.return_error(constants.ERR_NOT_INVITE)
            return
        print rt
        print invite['time']
        time_del = rt - invite['time']
        # 时间间隔太长
        if time_del > 24*3600*7:
            self.return_error(constants.ERR_TOO_LATE)
            return
        self.db.execute(
            "UPDATE `invite_re` SET `used` = 1 "
            "WHERE `id` = %s", invite['id'])
        self.db.execute(
            "INSERT INTO `invite_prize`(`uid`, `prize`, `type`, `invite_uid`)"
            "VALUES(%s, 200, 1, %s)", invite['uid'], self.current_user['id'])
        self.db.execute(
            "UPDATE `user` SET `invited_by` = %s "
            "WHERE `uid` = %s", invite['uid'], self.current_user['id'])
        self.db.execute(
            "UPDATE `user` SET `points` = `points` + 200, \
            `total_points` = `total_points` + 200, `invites` = `invites` + 1 "
            "WHERE `uid` = %s", invite['uid'])
        self.return_success()
