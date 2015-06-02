#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

有米广告回调处理
 @author lisongjian@youmi.net

"""
import utils, hashlib, datetime
from protocols import JSONBaseHandler
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class AdyoumiHandler(JSONBaseHandler):
    def get(self, platform):
        log_path = self.config['log']['adyoumi_log']
        utils.print_log('adyoumi', log_path, self.request.uri)
        if platform == 'adyoumi':
            self.__save_adyoumi_order()

    def __save_adyoumi_order(self):
        params = {}
        params['mac'] = self.get_argument('mac', '')
        params['andid'] = self.get_argument('android_id', '')
        params['callback_url'] = self.get_argument('callback_url', '')
        params['ei'] = self.get_argument('imei', '')
        params['si'] = self.get_argument('imsi', '')
        print params
        print params['callback_url']
        ei = params['ei'].encode("utf-8")
        si = params['si'].encode("utf-8")
        mac = params['mac'].encode("utf-8")
        andid = params['andid'].encode("utf-8")
        token = self.__get_devicefingerprinting(ei,si,mac,andid)
        print token
        token_info = self.db.get(
            "SELECT * FROM `wallad_clicks` WHERE `token`=%s LIMIT 1",token)
        if not token_info:
            self.db.execute(
                "INSERT INTO `wallad_clicks` (imei, imsi, mac, andid, token,callback_url, adserver,create_time)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s,%s)",
                ei, si, mac, andid, token, params['callback_url'], 1, datetime.datetime.now())
            self.return_success()
        else:
            self.write('already had token')

    def __get_devicefingerprinting(self, ei, si, mac, andid ):
        """简单的生成设备指纹方法"""
        valid_params = [
            ei,
            si,
            mac,
            andid,
        ]
        device_str = ':'.join(str(valid_params))
        return hashlib.md5(device_str).hexdigest()

