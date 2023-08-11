# -*- coding: utf-8 -*-
import io
import os
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pytest
import time

from environments.initConfig import initConfig


def send_email(file_new):
    # 读取html文件内容
    with io.open(file_new, 'rb') as fp:
        mail_body = fp.read()

    # 邮件内容, 格式, 编码
    msg = MIMEMultipart()

    username = 'app@kuainiu.io'  # 发件箱用户名
    password = 'GGxRo4g6'  # 发件箱密码
    sender = 'app@kuainiu.io'  # 发件人邮箱
    receiver = initConfig()
    # receiver = ['yuanxiujing@kuainiugroup.com', '1103686698@qq.com']  # 收件人邮箱
    print(receiver)
    smpt_server = 'hwsmtp.exmail.qq.com'
    port = 465

    # # 构造邮件附件
    # att1 = MIMEText(mail_body, _subtype='html', _charset='utf-8')
    # att1["Content-Type"] = 'application/octet-stream'
    # att1["Content-Disposition"] = 'attachment; filename="' + report_file_name
    # msg.attach(att1)

    # 构造邮件正文
    msg.attach(MIMEText(mail_body, _subtype='html', _charset='utf-8'))
    msg['From'] = sender
    msg['To'] = ';'.join(receiver)
    msg['Subject'] = Header("【贷后资产同步】接口自动化测试结果通知", 'utf-8').encode()

    try:
        smtp = smtplib.SMTP_SSL(smpt_server, port)
        smtp.login(username, password)
        print(21211)
        smtp.sendmail(sender, receiver, msg.as_string())
        print("发送邮件成功！！！")
        smtp.quit()
    except smtplib.SMTPException as e:
        print("发送邮件失败：" + e.__str__())


# ======查找测试目录，找到最新生成的测试报告文件======
def new_report(test_report):
    lists = os.listdir(test_report)  # 列出目录的下所有文件和文件夹保存到lists
    lists.sort(key=lambda fn: os.path.getmtime(test_report + "/" + fn))  # 按时间排序
    file_new = os.path.join(test_report, lists[-1])  # 获取最新的文件保存到file_new
    print(file_new)
    return file_new


if __name__ == '__main__':
    execute_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    # 测试报告文件夹
    report_path = os.path.join(execute_path, 'report')
    # 获取当前时间
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # 保存生成报告的路径
    report_file = os.path.join(report_path, 'dh_asset_sync_test_' + now + '.html')
    pytest.main(["-s", "-m", "dh_auto_test", f"{execute_path}", "--env=fox", "--environment=test", "-k", "foundation_test/case/dh",
                 f"--html={report_file}", "--self-contained-html"])
    new_report = new_report(report_path)
    # 发送测试报告
    send_email(new_report)
