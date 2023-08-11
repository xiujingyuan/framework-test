import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import os
import io


class EmailUtil:
    def __init__(self):
        pass

    @staticmethod
    def send_emal(report_path, report_file_name, *reciever, smpt_server='smtp.qq.com', port=465,
                  qq_code='fzrqxdlljaofccij', sender='1993715972@qq.com'):
        report_file = os.path.join(report_path, report_file_name)
        mail_title = '自动化测试报告:' + report_file_name

        # 读取html文件内容
        with io.open(report_file, 'rb') as fp:
            mail_body = fp.read()

        # 邮件内容, 格式, 编码
        msg = MIMEMultipart()

        # 构造邮件附件
        att1 = MIMEText(mail_body, _subtype='html', _charset='gbk')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="' + report_file_name
        msg.attach(att1)

        # 构造邮件正文
        msg.attach(MIMEText(mail_body, _subtype='html', _charset='gbk'))
        msg['From'] = sender
        msg['To'] = ';'.join(reciever)
        msg['Subject'] = Header(mail_title, 'utf-8')

        try:
            smtp = smtplib.SMTP_SSL(smpt_server, port)
            smtp.login(sender, qq_code)
            smtp.sendmail(sender, reciever, msg.as_string())
            print("发送邮件成功！！！")
            smtp.quit()
        except smtplib.SMTPException as e:
            print("发送邮件失败：" + e.__str__())


if __name__ == '__main__':
    report_path = os.environ["report_path"]
    report_name = os.environ['report_name']
    # report_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Report')
    EmailUtil.send_emal(report_path, 'main_function_test.html', *['katherinewang@kuainiugroup.com'])
