import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status, mixins, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

from .models import Mailbox, Template, Email
from .serializers import MailboxSerializer, TemplateSerializer, EmailSerializer
from .tasks import send_email_task
from .filters import EmailFilter


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'mailbox': reverse('mailbox-list', request=request, format=format),
        'template': reverse('template-list', request=request, format=format),
        'email': reverse('email', request=request, format=format),
    })


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


class EmailList(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    filterset_class = EmailFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            mailbox = Mailbox.objects.get(id=request.data['mailbox'])
        except KeyError as e:
            return Response(f'This field is required: {e}',
                            status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return Response(f'Chosen mailbox does not exist',
                            status=status.HTTP_400_BAD_REQUEST)

        if mailbox.is_active:
            serializer = EmailSerializer(data=request.data, many=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            email = serializer.data
            logging.debug('email added to db')

            template = Template.objects.get(id=email['template'])
            email_to_send = dict(
                id=email['id'],
                from_addr=mailbox.email_from + f' <{mailbox.login}>',
                to_addr='; '.join(email['to']),
                cc = '; '.join(email['cc']),
                bcc='; '.join(email['bcc']),
                reply_to=email['reply_to'],
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
