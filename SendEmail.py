import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr



class Send():
    def __init__(self):
        pass
    def _format_addr(self,s):
        # 参数格式化
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def _getfile(self):
        # 附件地址
        file = '/home/lsgo14/图片/img/'
        # now = datetime.datetime.now()
        # yesterday = now - datetime.timedelta(days=1)
        # yesterday = yesterday.strftime("%Y%m%d")
        # file = file + yesterday
        return [file+"FraLine.png", file+"TraLine.png", file+"KLine.png", file+"NKLine.png"]

    def addfile(self,msg):
        files =self._getfile()
        # 附件1
        attr1 = MIMEBase('image', 'png', filename='file.png')
        attr1.add_header('Content-Disposition', 'attachment',
                         filename=files[0][-11:])
        attr1.add_header('Content-ID', '<0>')
        attr1.add_header('X-Attachment-Id', '0')
        attr1.set_payload(open(files[0], 'rb+').read())
        encoders.encode_base64(attr1)
        msg.attach(attr1)

        # 附件2
        attr2 = MIMEBase('image', 'png', filename='file.png')
        attr2.add_header('Content-Disposition', 'attachment',
                         filename=files[1][-11:])
        attr2.add_header('Content-ID', '<0>')
        attr2.add_header('X-Attachment-Id', '0')
        attr2.set_payload(open(files[1], 'rb').read())
        encoders.encode_base64(attr2)
        msg.attach(attr2)

        # 附件3
        attr3 = MIMEBase('image', 'png', filename='file.png')
        attr3.add_header('Content-Disposition', 'attachment',
                         filename=files[1][-9:])
        attr3.add_header('Content-ID', '<0>')
        attr3.add_header('X-Attachment-Id', '0')
        attr3.set_payload(open(files[2], 'rb').read())
        encoders.encode_base64(attr3)
        msg.attach(attr3)

        # 附件4
        attr4 = MIMEBase('image', 'png', filename='file.png')
        attr4.add_header('Content-Disposition', 'attachment',
                         filename=files[1][-10:])
        attr4.add_header('Content-ID', '<0>')
        attr4.add_header('X-Attachment-Id', '0')
        attr4.set_payload(open(files[3], 'rb').read())
        encoders.encode_base64(attr4)
        msg.attach(attr4)


    def send(self, to_addr):
        from_addr = "1010151284@qq.com"  # 发件人 Email 地址和口令
        password = "************"
        smtp_server = "smtp.qq.com"  # SMTP 服务器地址
        # to_addr = "yanpengma@163.com"  # 收件人地址
        # to_addr = "adress1010151284@126.com"  # 收/件人地址

        # 邮件头
        msg = MIMEMultipart()
        msg['From'] = self._format_addr('lsgo <%s>' % from_addr)
        msg['To'] = self._format_addr('lsgo <%s>' % to_addr)
        msg['Subject'] = Header('沪深300', 'utf-8').encode()  # 标题

        # 邮件正文
        # msg.attach(MIMEText('……', 'plain', 'utf-8'))

        # 添加附件
        self.addfile(msg)

        try:
            server = smtplib.SMTP(smtp_server, 25)
            server.set_debuglevel(1)
            server.starttls()
            server.login(from_addr, password)
            server.sendmail(from_addr, [to_addr], msg.as_string())
            server.quit()
            print("邮件发送成功")
        except smtplib.SMTPException:
            self.send()
            print("Error: 发送邮件失败，正在重试！")
