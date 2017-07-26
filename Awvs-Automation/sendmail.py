#!/usr/bin/env python
# coding=utf-8

import smtplib
import time
from email.mime.text import MIMEText
from conf import mail_host, mail_user, mail_pass, mail_postfix


def send_main(to_mail, title, content):
    from_mail = "WvsScanner<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content, _subtype='plain', _charset='utf-8')
    msg['Subject'] = title
    msg['From'] = from_mail
    msg['To'] = ";".join(to_mail)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(from_mail, to_mail, msg.as_string())
        server.close()
        return True
    except Exception, e:
        catch_write(str(e))
        return False


def catch_write(err_code):
    file_name = "mail_error.txt"
    err_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    with open(file_name, 'a') as f:
        f.write(err_time + '\t' + err_code + '\n')

# 测试用
# if __name__ == "__main__":
#     mail_list = ['test@qq.com']
#     send_main(mail_list, '22', '22')
