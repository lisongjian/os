#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: lisongjian@youmi.net
#

"""游戏相关

"""
import protocols
import utils


class GameHandler(protocols.JSONBaseHandler):
    @protocols.unpack_arguments(with_scopeid=False)
    def get(self):
        log=self.arguments.get('referrer', 'zzy')
        log_path = self.config['log']['selfurl_log']
        utils.print_log('game', log_path, log)
        return self.return_result({"allow":True, "death_num": 2, "level":2})


