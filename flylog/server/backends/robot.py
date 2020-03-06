# -*- coding: utf-8 -*-
import json
import requests

from ..redis_helper import redis_default


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
    def __init__(self, web_hook_list):
        self.web_hook_list = web_hook_list

    def _is_reached_message_send_limit(self, content):
        """
        是否达到发送上限
        :param content:
        :return:
        """


    def emit(self, title, content):

        full_content = '\n\n'.join([title, content])
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({"msgtype": "text", "text": {"content": full_content}})

        res_list = []
        for web_hook in self.web_hook_list:
            rsp = requests.post(web_hook, data=data, headers=headers).json()
            res_list.append(rsp['errcode'] in [self.ERROR_CODE_KEYWORD, self.RET_OK])

        return False not in res_list
