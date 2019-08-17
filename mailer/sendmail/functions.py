from __future__ import absolute_import, unicode_literals
import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import os


def create_email(from_addr, to_addr, subject, body, cc=None, bcc= None, attachment=None):
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Cc'] = cc
    msg['Bcc'] = bcc
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # add attachment
    if attachment:
        filename = attachment.name.replace('attachments/', '')
        attachm = open(os.path.join('media/', attachment.name), 'rb')
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachm).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(p)

    return msg


def send_email(message, mailbox):
    if mailbox.use_ssl:
        with smtplib.SMTP_SSL(mailbox.host , mailbox.port) as server:
            print('loging')
            server.login(mailbox.login, mailbox.password)
            print('logged')
            server.send_message(message)
    else:
        with smtplib.SMTP(mailbox.host, mailbox.port) as server:
            print('running')
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(mailbox.login, mailbox.password)
            # server.sendmail(sender, to, msg)
            server.send_message(message)
    print('email sent')