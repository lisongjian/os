#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author chenjiehua@youmi.net
#
""" 反馈接口 """

import protocols
import constants


class FeedbackHandler(protocols.JSONBaseHandler):
    """ 用户反馈 """

    @protocols.unpack_arguments()
    def post(self):
        content = self.arguments.get("content")

        if not content:
            self.db.execute(
                "INSERT INTO `feedback`(`user`, `content`)"
                "VALUES(%s, %s)", self.current_user['id'], content)
            self.return_success()
        else:
            self.return_error(constants.ERR_PROTOCOL_ERROR)
