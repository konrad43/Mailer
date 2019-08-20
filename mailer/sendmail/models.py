import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField

class Mailbox(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.CharField(max_length=200)
    port = models.IntegerField(default=465)
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email_from = models.CharField(max_length=255)
    use_ssl = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    last_update = models.DateTimeField(auto_now=True, blank=True)

    @property
    def sent(self):
        return Email.objects.exclude(sent_date__exact=None).count()


class Template(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.CharField(max_length=255)
    text = models.TextField()
    attachment = models.FileField(upload_to='attachments/', blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    last_update = models.DateTimeField(auto_now=True, blank=True)


class Email(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mailbox = models.ForeignKey(Mailbox, on_delete=models.CASCADE, related_name='emails')
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='templates')
    to = ArrayField(models.EmailField(), default=list)
    cc = ArrayField(models.EmailField(), default=list, blank=True)
    bcc = ArrayField(models.EmailField(), default=list, blank=True)
    reply_to = models.EmailField(default=None, blank=True)
    sent_date = models.DateTimeField(default=None, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)