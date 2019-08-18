from __future__ import absolute_import, unicode_literals
import logging

from celery import shared_task
from celery.exceptions import MaxRetriesExceededError

from .functions import send_email, create_email

FORMAT = '%(levelname)s - %(asctime) %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT, filename='logs/email.log')

@shared_task(bind=True)
def send_email_task(self, email, mailbox):
    message = create_email(email)

    try:
        send_email(message, mailbox, email['id'])
    except Exception as e:
        import traceback
        logging.error(f'Email could not be send. Error: {e}')
        print(traceback.format_exc())
        logging.info(f'Could not send email from {email["from_addr"]} to {email["to_addr"]}')
        try:
            raise self.retry(countdown=30, max_retries=2)
        except MaxRetriesExceededError:
            logging.error('Could not send an email in 3 times')
