from __future__ import absolute_import, unicode_literals

from celery import shared_task

from .functions import send_email


@shared_task
def send_email_task():
    message = create_email(sender, to + to_addr, subject='dupa', body='mail testowy', cc=cc)
    if to_run == 1:
        with smtplib.SMTP_SSL(host , port_ssl) as server:
            print('loging')
            server.login(login, password)
            print('logged')
            server.sendmail(sender, to, msg)

    elif to_run == 2:
        with smtplib.SMTP(host, port) as server:
            print('running')
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(login, password)
            # server.sendmail(sender, to, msg)
            server.send_message(message)
    print('email sent')