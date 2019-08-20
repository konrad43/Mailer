import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Mailbox, Template, Email
from .serializers import MailboxSerializer, TemplateSerializer, EmailSerializer
from .tasks import send_email_task
from .filters import EmailFilter


class MailboxViewSet(viewsets.ModelViewSet):
    queryset = Mailbox.objects.all()
    serializer_class = MailboxSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    filterset_class = EmailFilter

    def create(self, request, *args, **kwargs):
        try:
            mailbox = Mailbox.objects.get(id=request.data['mailbox'])
            template = Template.objects.get(id=request.data['template'])
            cc = request.data.get('cc', [])
            bcc = request.data.get('bcc', [])
        except KeyError as e:
            return Response(f'This field is required: {e}',
                            status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return Response(f'Chosen mailbox or template does not exist',
                            status=status.HTTP_400_BAD_REQUEST)

        if mailbox.is_active:
            email = Email.objects.create(
                mailbox=mailbox,
                template=template,
                to=request.data['to'],
                cc=cc,
                bcc=bcc,
                reply_to=request.data.get('reply_to', None),
            )
            serializer = EmailSerializer(email, many=False)
            logging.debug('email added to db')

            email_to_send = dict(
                id=email.id,
                from_addr=mailbox.email_from + f' <{mailbox.login}>',
                to_addr='; '.join(email.to),
                cc = '; '.join(email.cc),
                bcc='; '.join(email.bcc),
                reply_to=email.reply_to,
                subject=template.subject,
                body=template.text,
                attachment=template.attachment.name,
            )
            print('Sending email')
            send_email_task.delay(email_to_send, mailbox.id)
        else:
            return Response('Your mailbox is not active',
                            status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        return Response('Method not allowed',
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response('Method not allowed',
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

