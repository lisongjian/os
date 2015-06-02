#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author zhengji@youmi.net
#
""" 反馈接口 """

import protocols
import constants
import utils
import sys
reload (sys)
sys.setdefaultencoding('utf-8')


class FeedbackHandler(protocols.JSONBaseHandler):
    """ 用户反馈 """

    @protocols.unpack_arguments(with_scopeid=False)
    def post(self):
        content = self.arguments.get('content', "")
        mail = self.arguments.get('mail', "")
        scopeid = self.arguments.get('scopeid', "")

        if  content:
            self.db.execute(
                "INSERT INTO `feedback`(`scopeid`, `content`,`mail`,`appType`)"
                "VALUES(%s, %s, %s, 1)", scopeid, content, mail)
            self.return_success()
        else:
            self.return_error(constants.ERR_PROTOCOL_ERROR)

class ShareHandler(protocols.JSONBaseHandler):
    """分享应用"""

    @protocols.unpack_kakaarguments_byscopeid()
    def get(self):
        sharepoint = self.db.get("SELECT * FROM `options` WHERE `key` = 'share'")
        type = self.arguments.get('type')
        print type
        share = self.db.get(
        "SELECT `share_fb`,`share_tw`,`share_gg`,`like` FROM `user` WHERE `uid`=%s", self.current_user['uid'])
        if (share['share_fb']==0 and type=="1") or (share['share_tw']==0 and type=="2") or (share['share_gg']==0 and type=="3"):
            prize = int(sharepoint['values'])
            self.db.execute(
                "UPDATE `user` SET `points` = `points` + %s, \
                `total_points` = `total_points` + %s , \
                `share_points` = `share_points`+ %s "
                "WHERE `scopeid` = %s"  %(prize, prize, prize, self.arguments.get('scopeid')))
            if type=="1":
                self.db.execute(
                "UPDATE `user` SET `share_fb` = 1 WHERE `uid`=%s", self.current_user['uid'])
            elif type=="2":
                self.db.execute(
                "UPDATE `user` SET `share_tw` = 1 WHERE `uid`=%s", self.current_user['uid'])
            elif type=="3":
                self.db.execute(
                "UPDATE `user` SET `share_gg` = 1 WHERE `uid`=%s", self.current_user['uid'])
            order="分享紅利"
            ad="分享紅利"
            self.db.execute(
                "INSERT INTO `callback_order`(`order`,`ad`,`user`,`platform`,`ad_source`,`points`,`appType`)"
                "VALUES(%s,%s,%s,%s,%s,%s,1)", order,ad,self.current_user['uid'],3,2,prize)
            self.db.execute(
                "INSERT INTO `global_orders` (uid, points, last, type, note,appType)"
                "VALUES (%s, %s, %s, %s, %s, 1)",
                self.current_user['uid'], prize, self.current_user['points'], 2, ad)
        elif (share['like']==0 and type=="4"):
            likepoint = self.db.get("SELECT * FROM `options` WHERE `key` ='like'")
            prize = int(likepoint['values'])
            self.db.execute(
                "UPDATE `user` SET `points` = `points` + %s, \
                `total_points` = `total_points` + %s , \
                `share_points` = `share_points`+ %s , \
                `like` = '1'"
                "WHERE `scopeid` = %s"  %(prize, prize, prize, self.arguments.get('scopeid')))
            order="fb點贊紅利"
            ad="fb點贊紅利"
            self.db.execute(
                "INSERT INTO `callback_order`(`order`,`ad`,`user`,`platform`,`ad_source`,`points`,`appType`)"
                "VALUES(%s,%s,%s,%s,%s,%s,1)", order,ad,self.current_user['uid'],3,11,prize)
            self.db.execute(
                "INSERT INTO `global_orders` (uid, points, last, type, note,appType)"
                "VALUES (%s, %s, %s, %s, %s, 1)",
                self.current_user['uid'], prize, self.current_user['points'], 11, ad)

        else:
            prize = 0
        user_info=self.db.get(
        "SELECT `points` from `user` WHERE `uid` = %s", self.current_user['uid'])
        log_path = self.config['log']['fblike_log']
        utils.print_log('fblike', log_path, self.request.uri+"uid="+str(self.current_user['uid'])+"points="+str(prize))
        self.return_result({
            "points":user_info['points'],
            "bonus":prize,
        })
