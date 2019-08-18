from rest_framework import serializers

from .models import Mailbox, Template, Email

class MailboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailbox
        fields = ['host', 'email_from', 'use_ssl', 'is_active', 'sent',
                  'last_update']


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ['subject', 'text', 'date']


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['mailbox', 'template', 'to', 'cc', 'reply_to',
                  'sent_date']