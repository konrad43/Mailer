from __future__ import absolute_import, unicode_literals
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import os, logging, smtplib, datetime

from .models import Mailbox, Email


logging.basicConfig(level=logging.INFO, format=FORMAT, filename='logs/email.log')
# logging.basicConfig(level=logging.DEBUG)

def create_email(email):
    print('creating email')
    try:
        msg = MIMEMultipart()
        msg['From'] = email['from_addr']
        msg['To'] = email['to_addr']
        msg['Cc'] = email['cc']
        msg['Bcc'] = email['bcc']
        msg['Subject'] = email['subject']
        msg.attach(MIMEText(email['body'], 'plain'))
        attachment = email['attachment']

        # add attachment
        if attachment:
            filename = attachment.replace('attachments/', '')
            attachm = open(os.path.join('media/', attachment), 'rb')
            p = MIMEBase('application', 'octet-stream')
            p.set_payload((attachm).read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', f'attachment; filename={filename}')
            msg.attach(p)
        return msg

    except Exception as e:
        logging.error(f'Email could not be created. Error: {e}')


def send_email(email, mailbox, email_id):
    mailbox = Mailbox.objects.get(id=mailbox)
    if mailbox.use_ssl:
        with smtplib.SMTP_SSL(mailbox.host , mailbox.port) as server:
            print('loging')
            server.login(mailbox.login, mailbox.password)
            print('logged')
            server.send_message(email)
    else:
        with smtplib.SMTP(mailbox.host, mailbox.port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            print('loging')
            server.login(mailbox.login, mailbox.password)
            server.send_message(email)
    print('email sent')
    email_sent = Email.objects.get(id=email_id)
    email_sent.sent_date = datetime.datetime.now()
    email_sent.save()
    print('sent date updated')
