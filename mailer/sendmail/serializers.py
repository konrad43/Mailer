from rest_framework import serializers

from .models import Mailbox, Template, Email

class MailboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailbox
        fields = ['id', 'host','port', 'login', 'password', 'email_from', 'use_ssl',
                  'is_active', 'last_update', 'date', 'sent']


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ['id', 'subject', 'text', 'attachment', 'date', 'last_update']


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['id', 'mailbox', 'template', 'to', 'cc', 'bcc', 'reply_to',
                  'sent_date', 'date']