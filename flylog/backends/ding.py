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

        rsp = self._send_message(full_content, agent_id, user_list, party_list)

        assert rsp['errcode'] == 0, rsp

    def _get_token(self):
        """
        获取access_token
        http返回格式: {"access_token":"xxxx","errcode":0,"errmsg":"ok"}
        """

        url = '%s://%s%s' % (self.SCHEMA, self.HOST, self.URL_PATH_GET_TOKEN)

        return requests.get(
            url,
            params=dict(
                corpid=self.corp_id,
                corpsecret=self.corp_secret,
            ),
            headers=self.HEADERS
        ).json()

    def _send_message(self, content, agent_id, user_list=None, party_list=None):
        """
        发送消息
        """

        access_token = self._get_token()['access_token']

        url = '%s://%s%s' % (self.SCHEMA, self.HOST, self.URL_PATH_SEND_MESSAGE)

        user_list = [str(it) for it in user_list or []]
        party_list = [str(it) for it in party_list or []]

        return requests.post(
            url,
            data=dict(
                touser='|'.join(user_list),
                toparty='|'.join(party_list),
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
        ).json()

    def _get_department_list(self):
        """
        获取部门列表
        """

        access_token = self._get_token()['access_token']

        url = '%s://%s%s' % (self.SCHEMA, self.HOST, self.URL_PATH_DEPARTMENT_LIST)

        return requests.get(
            url,
            params=dict(
                access_token=access_token
            ),
            headers=self.HEADERS
        ).json()

    def _get_department_user_list(self, department_id):
        """
        获取部门成员列表
        如果要获取顶层公司成员，好像传1就行
        """

        access_token = self._get_token()['access_token']

        url = '%s://%s%s' % (self.SCHEMA, self.HOST, self.URL_PATH_DEPARTMENT_LIST)

        return requests.get(
            url,
            params=dict(
                access_token=access_token,
                department_id=department_id,
            ),
            headers=self.HEADERS
        ).json()