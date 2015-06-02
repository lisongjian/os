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
import utils

class TopHandler(protocols.JSONBaseHandler):
    """ 邀请人排行榜 """

    @protocols.unpack_arguments()
    def get(self):
        top = self.db.query(
            "SELECT `uid`, `invites` FROM `user` "
            "WHERE `invites`>0 ORDER BY `invites` DESC LIMIT 20")

        self.return_result({"top": top})


class DownloadHandler(protocols.JSONBaseHandler):
    """ 下载链接跳转 """

    @protocols.unpack_arguments()
    def get(self):
        pname = self.arguments.get('pname',"")
        channel = self.arguments.get('channel',"")
        print pname
        print channel
        platform = self.arguments.get('platform')
        download = self.db.get(
            "SELECT `download_url` FROM `changelogs` "
            "WHERE `platform` = %s ORDER BY `release_time` "
            "DESC LIMIT 1", platform)

        if not download:
            self.write("出错啦～～～")
            return
        '''
        self.db.execute(
            "INSERT INTO `invite_re`(`uid`, `ip`)"
            "VALUES(%s, %s)", self.current_user['id'],  self.request.headers.get('X-Real-Ip', None).split(',')[0])
        '''
        self.redirect(download['download_url'])


class CheckInviteHandler(protocols.JSONBaseHandler):
    """ 填写邀请码 """

    @protocols.unpack_arguments()
    def get(self):
        #token = self.arguments.get('token')
        log_path = self.config['log']['invite_log']
        #utils.print_log('invite', log_path, self.request.uri)
        scopeid = self.arguments.get('scopeid')
        #被谁邀请
        invitecode = self.arguments.get('invitecode')

        user=self.db.get(
                    "SELECT `uid`, `scopeid`,`points`, `invites` from `user` \
                    WHERE `invited_code` = %s AND `appType`=1",
                    invitecode)
        if user:
            user=self.db.get(
                "SELECT * FROM `user` WHERE `invited_code` = %s AND `scopeid` = %s AND `appType`=1",
                invitecode, user['scopeid'])
        if not user:
            self.return_error(constants.ERR_NOT_INVITE, "没有此邀请码")
            return
        if scopeid==user['scopeid']:
            self.return_error(constants.ERR_NOT_SELF, "不能邀请自己")
            return
        if self.current_user['invited_by'] != None:
            self.return_error(constants.ERR_NOT_NULL, "邀请码已填过")
            return
        else:
            invite_prize=self.db.get("SELECT * FROM `options` WHERE `key`='invite_reg_prize'")
            prize = int(invite_prize['values'])
            order="邀請紅利"
            ad="邀請紅利"
            #给邀请人加积分
        InviteCheat = self.db.get(
            "SELECT count(*) FROM `callback_order` WHERE `user` = %s AND `ad_source` = '3' AND DATE(`time`)=CURDATE()",
            user['uid'])
        utils.print_log('invite', log_path, self.request.uri+"&kaka&byInviteUid="+str(user['uid'])+"&InviteUid="+str(self.current_user['uid']))
        maxInvite = self.db.get("SELECT * FROM `options` WHERE `key` = 'maxInvite'")
        totalInvite = self.db.get(
            "SELECT count(*) FROM `callback_order` WHERE `user`= %s AND `ad_source` = '3'",
            user['uid'])
        if InviteCheat:
            if InviteCheat['count(*)']<5:
                # 限制总邀请人数
                if totalInvite['count(*)'] < maxInvite['values']:
                   # 给邀请人加积分
                    self.db.execute(
                        "UPDATE `user` SET `invites` = `invites`+ 1, `invite_points`=`invite_points`+%s, `points`=`points`+%s, total_points=`total_points`+%s "
                        "WHERE `invited_code` = %s", prize,prize,prize, invitecode)
                    self.db.execute(
                        "INSERT INTO `callback_order`(`order`,`ad`,`user`,`platform`,`ad_source`,`points`,`appType`)"
                        "VALUES(%s,%s,%s,%s,%s,%s,1)", order,ad,user['uid'],3,3,prize)
                    self.db.execute(
                        "INSERT INTO `global_orders` (uid, points, last, type, note,appType)"
                        "VALUES (%s, %s, %s, %s, %s, 1)",
                        user['uid'], prize, user['points'], 3, ad+"邀请uid"+str(self.current_user['uid']))
                # 给新用户加积分
                self.db.execute(
                    "UPDATE `user` SET `invited_by` = %s, `invite_points`=`invite_points`+%s, `points`=`points`+%s, total_points=`total_points`+%s "
                    "WHERE `scopeid` = %s", invitecode, prize,prize,prize, scopeid)
                self.db.execute(
                    "INSERT INTO `callback_order`(`order`,`ad`,`user`,`platform`,`ad_source`,`points`,`appType`)"
                    "VALUES(%s,%s,%s,%s,%s,%s,1)", order,ad,self.current_user['uid'],3,3,prize)
                self.db.execute(
                    "INSERT INTO `global_orders` (uid, points, last, type, note,appType)"
                    "VALUES (%s, %s, %s, %s, %s,1)",
                self.current_user['uid'], prize, self.current_user['points'], 3, ad+"被uid邀请"+str(user['uid']))
            self.return_success()

