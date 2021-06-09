# -*- coding+: utf-8 -*-
"""
@author:Kirito
@file:emailer.py
@time:2021/06/08
@describe：邮件发送模块:多个附件使用list[]
"""
from Comm.logger import Logger
from Config.yamlReader import email_cfg,smtp_cfg
import smtplib, os
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


class Email():
    # 文件大小
    _file_size = 20
    # 文件数量
    _file_count = 10

    def __init__(self, subject, context=None, attachment=None):
        '''
        构造函数
        :param subject:邮件标题
        :param context:邮件正文
        :param attachment:邮件附件
        多个附件使用list[]
        '''
        self.logger = Logger().logger
        self.logger.info(("*" * 25) + " Emailer.__init__() " + ("*" * 25))
        self.subject = subject
        self.context = context
        self.attachment = attachment
        # 发送带附件的邮件，首先要创建MIMEMultipart()实例，然后构造附件，如果有多个附件，可依次构造，
        # 最后利用smtplib.smtp发送。
        self.message = MIMEMultipart()
        self.message_init()
        self.logger.info(("*" * 25) + " Emailer.__init__() " + ("*" * 25))
    def message_init(self):
        '''
        邮件内容处理
        :return: None
        '''
        self.logger.info(("*" * 25) + " Emailer.message_init(邮件内容处理) " + ("*" * 25))
        # 邮件标题
        if self.subject:
            self.message['Subject'] = Header(self.subject, 'utf-8')
        else:
            raise ValueError(f"无效的标题：{self.subject}，请输入正确的标题！")
            self.logger.error(f"无效的标题：{self.subject}，请输入正确的标题！")
        #邮件发送人
        self.message['Form'] = email_cfg['sender']
        #邮件收件人
        self.message['To'] = email_cfg['receivers']
        #邮件正文信息
        if self.context:
            self.message.attach(MIMEText(self.context,'html','utf-8'))
        else:
            raise ValueError(f"无效的正文：{self.context}，请输入正确的正文！")
            self.logger.error(f"无效的正文：{self.subject}，请输入正确的正文！")
        #邮件附件
        if self.attachment:
            # isinstance() 函数来判断一个对象是否是一个已知的类型;判断是否为单个文件
            if isinstance(self.attachment, str):
                self.attach_handle(self.attachment)
            #判断是否为多个附件
            if isinstance(self.attachment, list):
                count = 0
                # 循环多个文件
                for each in self.attachment:
                    # 判断文件数量是否等于小于预设值
                    if count <= self._file_count:
                        self.attach_handle(each)
                        count += 1
                    else:
                        self.logger.warning(f"附件数量超过预设值：{self._file_count}个")
                        break
        self.logger.info('邮件内容组装完成～')
        self.logger.info(("*" * 25) + " Emailer.message_init(邮件内容处理) " + ("*" * 25))

    def attach_handle(self,file):
        '''
        附件处理
        :param file:附件
        :return: none
        '''
        self.logger.info(("*" * 25) + " Emailer.attach_handle(附件处理) " + ("*" * 25))
        # 判断是否为文件并且大小是否符合预设值
        if os.path.isfile(file) and os.path.getsize(file) <= self._file_size * 1024 * 1024:
            attach = MIMEApplication(open(file, 'rb').read())
            attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            attach["Content-Type"] = 'application/octet-stream'
            self.message.attach(attach)
            self.logger.info('附件处理完成～')
        else:
            self.logger.error(f'附件超过{self._file_size}M，或者{file}不存在')
        self.logger.info(("*" * 25) + " Emailer.attach_handle(附件处理) " + ("*" * 25))

    def send_email(self):
        '''
        发送邮件
        :return: 发送结果
        '''
        self.logger.info(("*" * 25) + " Emailer.send_email(发送邮件) " + ("*" * 25))
        try:
            # 创建邮件发送连接(smtp有两个端口号：465.587)
            conn = smtplib.SMTP_SSL(smtp_cfg['host'], int(smtp_cfg['port']))
            self.logger.info(f"连接邮箱成功～host:{smtp_cfg['host']},port:{smtp_cfg['port']}")
        except:
            self.logger.error(f"连接邮箱失败,请检查配置信息是否正确～host:{smtp_cfg['host']},port:{smtp_cfg['port']}")
        # 邮件发送结果变量
        result = True
        try:
            # 登陆邮件
            conn.login(smtp_cfg['user'], smtp_cfg['pwd'])
            self.logger.info('登陆邮箱成功～  登陆用户名：{}'.format(smtp_cfg['user']))
            conn.sendmail(email_cfg['sender'], email_cfg['receivers'], self.message.as_string())
            self.logger.info("获取发件人信息成功：{0},获取收件人成功:{1}".format(email_cfg['sender'], email_cfg['receivers']))
            self.logger.info('邮件发送成功～')
        except smtplib.SMTPAuthenticationError:
            result = False
            self.logger.error("登陆邮箱失败～请检查账号密码是否正确！", exc_info=True)
        except smtplib.SMTPException:
            result = False
            self.logger.error("发送邮件失败！", exc_info=True)
        finally:
            conn.close()
            self.logger.info('正在关闭邮箱连接～')
        self.logger.info(("*" * 25) + " Emailer.send_email(发送邮件) " + ("*" * 25))
        return result

if __name__ == '__main__':
    mail = Email('测试组第三周周报','第一次发送',attachment=['/Users/air/PycharmProjects/GtmshTestFrame/Config/config.yaml','/Users/air/PycharmProjects/GtmshTestFrame/Log/log.log'])
    send = mail.send_email()






