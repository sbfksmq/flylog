# -*- coding: utf-8 -*-


class MailBackend(object):
    """
    发送邮件
    """

    def __init__(self, host, port, username, password, sender, use_ssl, use_tls):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.sender = sender
        self.use_ssl = use_ssl
        self.use_tls = use_tls

    def emit(self, title, content, receiver_list):
        """
        发送
        """

        self._sendmail(self.host, self.port, self.sender, receiver_list, title, content,
                       username=self.username, password=self.password,
                       use_ssl=self.use_ssl, use_tls=self.use_tls
                       )

    def _sendmail(self, host, port, sender, receiver_list, subject, content,
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
        mail_msg['To'] = ', '.join(receiver_list)
        mail_msg['Date'] = formatdate()

        if use_ssl:
            mail_client = smtplib.SMTP_SSL(host, port)
        else:
            mail_client = smtplib.SMTP(host, port)

        mail_client.set_debuglevel(debuglevel)

        if use_tls:
            mail_client.starttls()

        if username and password:
            mail_client.login(username, password)

        # 发邮件
        mail_client.sendmail(sender, receiver_list, mail_msg.as_string())
        mail_client.quit()
