# encoding: utf-8

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import json

from CommonLogging import CommonLogging

commlogger = CommonLogging().getlog()

# sender = 'example@example.com'
# receivers = ['receiver@example.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
 
# # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
# message = MIMEText('send email test. 发生邮件测试。', 'plain', 'utf-8')
# message['From'] = Header("sender 发送者", 'utf-8')   # 发送者
# message['To'] =  Header("receiver 接收者", 'utf-8')        # 接收者
 
# subject = 'test subject 测试主题'
# message['Subject'] = Header(subject, 'utf-8')
 
# try:
#     smtpObj = smtplib.SMTP('localhost')
#     smtpObj.sendmail(sender, receivers, message.as_string())
#     print "邮件发送成功"
# except smtplib.SMTPException:
#     print "Error: 无法发送邮件"


def SendEmail(from_header, to_addr, email_msg, subject):
    # 发信方的信息：发信邮箱，邮箱授权码
    # 读取json
    f = open("/home/app/secrets/smtp-config.json",'r',encoding='utf-8')
    smtpSender = json.load(f)
    f.close()
    try:
        from_addr = smtpSender['sender_addr']
        password = smtpSender['password']
    except Exception as e:
        commlogger.warning("catch exception: " + str(e))
        commlogger.info("stop send_email")
        return
            
    # 发信服务器
    smtp_server = 'smtp.office365.com'
    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg = MIMEText(email_msg, 'plain', 'utf-8')

    # 邮件头信息
    # msg['From'] = Header(from_addr)
    msg['From'] = Header(from_header)
    if type(to_addr) is str:
        msg['To'] = Header(to_addr)
    elif type(to_addr) is list:
        msg['To'] = Header(";".join(to_addr))  # 由于当群发时，to_addr是个list，转化为str
    msg['Subject'] = Header(subject)

    try:
        # 开启发信服务，这里使用的是tls加密传输
        server = smtplib.SMTP(smtp_server,587)
        # server.set_debuglevel(True) # 查看实时登录日志信息
        server.ehlo()
        server.starttls()#   starttls()来建立安全连接
        server.ehlo()
        server.login(from_addr,password)

        # # 开启发信服务，这里使用的是ssl加密传输
        # server = smtplib.SMTP_SSL(smtp_server)
        # server.connect(smtp_server, 465)  # 465为ssl 加密 SMTP端口
        # # 登录发信邮箱
        # server.login(from_addr, password)

        # 发送邮件
        server.sendmail(from_addr, to_addr, msg.as_string())
        # 关闭服务器
        server.quit()
        commlogger.info("send email sucess")
    except smtplib.SMTPException:
        commlogger.error("Error: exception 无法发送邮件")

# if __name__ == '__main__':
#     commlogger.info("start email send")
#     mailContentFile = open('Mail-Content_en.txt', 'r', encoding='utf-8')
#     mailContent = mailContentFile.read()
#     mailContentFile.close()
#     SendEmail('dxx auto notice', 'example@example.com', mailContent, 'dxx weekly result')