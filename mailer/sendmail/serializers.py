from rest_framework import serializers

from .models import Mailbox, Template, Email

class MailboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailbox
        fields = '__all__'


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = '__all__'
