#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
用来作为接受log传递的agent
通过udp通道。
"""

import json
import logging
import logging.config
import SocketServer

logger = logging.getLogger('flylog')


class FlyLogAgent(object):
    debug = False

    def __init__(self, config=None, debug=None):
        self.config = config
        if debug is not None:
            self.debug = debug

    def sendmail(self, server, port, sender, receivers, subject, content,
                 content_type='plain', encoding='utf-8',
                 username=None, password=None, use_ssl=False, use_tls=False, debuglevel=0
                 ):
        """
        发送邮件
        content_type: plain / html
        """
        import smtplib
        from email.mime.text import MIMEText
        from email.header import Header
        from email.utils import formatdate

        mail_msg = MIMEText(content, content_type, encoding)
        mail_msg['Subject'] = Header(subject, encoding)
        mail_msg['From'] = sender
        mail_msg['To'] = ', '.join(receivers)
        mail_msg['Date'] = formatdate()

        if use_ssl:
            mail_client = smtplib.SMTP_SSL(server, port)
        else:
            mail_client = smtplib.SMTP(server, port)

        mail_client.set_debuglevel(debuglevel)

        if use_tls:
            mail_client.starttls()

        if username and password:
            mail_client.login(username, password)

        # 发邮件
        mail_client.sendmail(sender, receivers, mail_msg.as_string())
        mail_client.quit()

    def handle_message(self, message, address):
        recv_dict = json.loads(message)

        role_list = recv_dict.get('role_list')

        if role_list is None:
            # 如果role_list为null，就代表走默认的receiver_list
            mail_receiver_list = self.config.MAIL_RECEIVER_LIST
        else:
            # 否则配置了什么就是什么
            mail_receiver_list = []
            for role, receiver_list in getattr(self.config, 'MAIL_ROLE_TO_RECEIVER_LIST', dict()).items():
                if role in role_list:
                    mail_receiver_list.extend(receiver_list)

            mail_receiver_list = list(set(mail_receiver_list))

        if not mail_receiver_list:
            # 如果没有接收者，就直接返回了
            return

        try:
            self.sendmail(self.config.MAIL_SERVER, self.config.MAIL_PORT, self.config.MAIL_SENDER, mail_receiver_list,
                          u'[%s]Attention!' % recv_dict.get('source'), recv_dict.get('content'),
                          username=self.config.MAIL_USERNAME, password=self.config.MAIL_PASSWORD,
                          use_ssl=self.config.MAIL_USE_SSL, use_tls=self.config.MAIL_USE_TLS)
        except:
            logger.error("exc occur. message: %r", message, exc_info=True)

    def run(self, host, port):
        class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
            def handle(sub_self):
                message = sub_self.request[0]
                try:
                    self.handle_message(message, sub_self.client_address)
                except:
                    logger.error('exc occur.', exc_info=True)

        server = SocketServer.ThreadingUDPServer((host, port), ThreadedUDPRequestHandler)

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        except:
            logger.error('exc occur.', exc_info=True)
