import logging
import datetime

from rest_framework import viewsets
from rest_framework.response import Response

from .models import Mailbox, Template, Email
from .serializers import MailboxSerializer, TemplateSerializer, EmailSerializer
from .tasks import send_email_task
from .functions import create_email


class MailboxViewSet(viewsets.ModelViewSet):
    queryset = Mailbox.objects.all()
    serializer_class = MailboxSerializer


class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer


class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer

    def create(self, request, *args, **kwargs):
        mailbox = Mailbox.objects.get(id=request.data['mailbox'])
        template = Template.objects.get(id=request.data['template'])
        cc = request.data.get('cc', [])
        bcc = request.data.get('bcc', [])

        email = Email.objects.create(
            mailbox=mailbox,
            template=template,
            to=request.data['to'],
            cc=cc,
            bcc=bcc,
            reply_to=request.data.get('reply_to', None),
            sent_date=datetime.datetime.now()
        )

        serializer = EmailSerializer(email, many=False)
        logging.info('email added to db')

        to_addr = '; '.join(email.to)
        copy = '; '.join(email.cc)
        b_copy = '; '.join(email.bcc)

        email_to_send = create_email(
            from_addr=mailbox.email_from + f' <{mailbox.login}>',
            to_addr=to_addr,
            cc = copy,
            bcc=b_copy,
            subject=template.subject,
            body=template.text,
            attachment=template.attachment
        )

        print(email_to_send)
        # send_email_task()
        return Response(serializer.data)
