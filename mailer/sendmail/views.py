import logging

from rest_framework import viewsets
from rest_framework.response import Response
from django.http import HttpResponse

from .models import Mailbox, Template, Email
from .serializers import MailboxSerializer, TemplateSerializer, EmailSerializer
from .tasks import send_email_task


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
            # sent_date=datetime.datetime.now()
        )
        serializer = EmailSerializer(email, many=False)
        logging.debug('email added to db')

        email_to_send = dict(
            id=email.id,
            from_addr=mailbox.email_from + f' <{mailbox.login}>',
            to_addr='; '.join(email.to),
            cc = '; '.join(email.cc),
            bcc='; '.join(email.bcc),
            subject=template.subject,
            body=template.text,
            attachment=template.attachment.name
        )
        if mailbox.is_active:
            print('Sending email')
            # send_email_task.delay(email_to_send, mailbox.id)
            send_email_task(email_to_send, mailbox.id)
        else:
            return HttpResponse('Your mailbox is not active')

        return Response(serializer.data)

