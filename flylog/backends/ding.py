# -*- coding: utf-8 -*-

import requests


class DingBackend(object):
    """
    钉钉
    """

    SCHEMA = 'https'
    HOST = 'oapi.dingtalk.com'
    HEADERS = {
        'Content-Type': 'application/json'
    }

    # 获取token
    URL_PATH_GET_TOKEN = '/gettoken'
    # 发送消息
    URL_PATH_SEND_MESSAGE = '/message/send'
    # 获取部门列表
    URL_PATH_DEPARTMENT_LIST = '/department/list'
    # 获取部门成员列表
    URL_PATH_USER_LIST = '/user/list'

    def __init__(self, corp_id, corp_secret):
        self.corp_id = corp_id
        self.corp_secret = corp_secret

    def emit(self, title, content, agent_id, user_list=None, party_list=None):
        """
        发送
        """

        full_content = '\n'.join([title, content])

        return self._send_message(full_content, agent_id, user_list, party_list)

    def _get_token(self):
        """
        获取access_token
        http返回格式: {"access_token":"xxxx","errcode":0,"errmsg":"ok"}
        """

        url = '%s://%s%s' % (self.SCHEMA, self.HOST, self.URL_PATH_GET_TOKEN)

        return requests.get(
            url,
            headers=self.HEADERS
        ).json()['access_token']

    def _send_message(self, content, agent_id, user_list=None, party_list=None):
        """
        发送消息
        """

        access_token = self._get_token()

        url = '%s://%s%s' % (self.SCHEMA, self.HOST, self.URL_PATH_SEND_MESSAGE)

        return requests.post(
            url,
            data=dict(
                touser='|'.join(user_list or []),
                toparty='|'.join(party_list or []),
                agentid=agent_id,
                msgtype='text',
                text=dict(
                    content=content
                )
            ),
            params=dict(
                access_token=access_token
            ),
            headers=self.HEADERS
        ).json()['access_token']
