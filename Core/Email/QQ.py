#!/usr/bin/python3
#coding:utf-8

import smtplib
import os
from email.mime.text import MIMEText
# from email.header import Header
from .Interfacex import Interfacex

# QQ发送实例

class QQClass(Interfacex) :

    def send(self, to) :
        # 发送方账号
        sender = os.environ.get('EMAIL_QQ','10086') + '@qq.com'
        # 密码
        password = os.environ.get('Email_PWD','10086')

        msg = MIMEText(self.get_content(), _subtype='html',_charset='utf-8')
        msg['Subject'] = self.get_title()
        msg['From'] = sender
        msg['To'] = to

        try:
            #邮件服务器及端口号
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            #登录SMTP服务器　　　　　　　
            s.login(sender, password) 
            #发邮件 as_string()把MIMEText对象变成str                               
            s.sendmail(sender, to, msg.as_string())
            return True
        except s.SMTPException:
            raise Exception("send fail", 11001)
        finally:
            s.quit()