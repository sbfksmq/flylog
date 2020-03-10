# -*- coding: utf-8 -*-
import json
import requests
import re

from ..log import logger
from ..redis_helper import FlylogMsgCache


class DingRobot(object):

    ERROR_CODE_KEYWORD = 310000
    RET_OK = 0

    """
    todo 
    1 redis 缓存类
    2 filter接口 以文件名 行号,日志内容的md5值为key, 发送次数为value 存储 (是否要每天清零)
    3 正则表达式的匹配截取 ：文件名, 行号，日志内容 
    
    [g_p_h_mtt@iZgw8izpv8a5yktv7kz6v9Z]Attention!
    /--------------------------------------------------------------------------------
    [CRITICAL][2020-03-05 21:28:39,563][18620:139919643383552][mtt_hall.py:47 user_enter]:
    mtt user enter patch, empty event id, uid: 27562, req: event_id: 0
    desk_id: 2972264
    view_openid: "27578"
    group_id: 0

    --------------------------------------------------------------------------------/
    """
    def __init__(self, web_hook_list, resend_times=1):
        self.web_hook_list = web_hook_list
        self.resend_times = resend_times

    def _is_reached_message_send_limit(self, info):
        """
        是否达到发送上限
        :param info:
        :return:
        """
        msg_md = ''
        times = FlylogMsgCache(info, msg_md).get_times()
        return times < self.resend_times

    @staticmethod
    def find_info(content):
        """
        提取content中 文件名 行号 函数名 组成 的字符
        :param content:
        :return:
        """
        pattern = re.compile('[[](.*?)[]]', re.S)
        res_list = re.findall(pattern, content)
        if not res_list or len(res_list) < 4:
            return ''
        return res_list[4]

    def emit(self, title, content):

        full_content = '\n\n'.join([title, content])
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({"msgtype": "text", "text": {"content": full_content}})

        info = self.find_info(content)
        if not info:
            logger.error('file info invalid content info: %s', content)
            return False

        if self._is_reached_message_send_limit(info):
            logger.error('log info reached resend limit content: %s', content)
            return True

        res_list = []
        for web_hook in self.web_hook_list:
            rsp = requests.post(web_hook, data=data, headers=headers).json()
            res_list.append(rsp['errcode'] in [self.ERROR_CODE_KEYWORD, self.RET_OK])

        return False not in res_list
