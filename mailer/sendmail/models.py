from django.db import models
from django.contrib.postgres.fields import ArrayField

class Mailbox(models.Model):
    host = models.CharField(max_length=200)
    port = models.IntegerField(default=465)
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email_from = models.CharField(max_length=255)
    use_ssl = models.BooleanField()
    is_active = models.BooleanField(default=False, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    last_update = models.DateTimeField(auto_now=True, blank=True)

    def sent(self):
        return Email.objects.exclude(sent_date__exact=None).count()


class Template(models.Model):
    subject = models.CharField(max_length=255)
    text = models.TextField()
    attachment = models.FileField(upload_to='attachments/', blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    last_update = models.DateTimeField(auto_now=True, blank=True)


class Email(models.Model):
    mailbox = models.ForeignKey(Mailbox, on_delete=models.CASCADE, related_name='emails')
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='templates')
    to = ArrayField(models.CharField(max_length=200), default=list)
    cc = ArrayField(models.CharField(max_length=200), default=list, blank=True)
    bcc = ArrayField(models.CharField(max_length=200), default=list, blank=True)
    reply_to = models.EmailField(default=None)
    sent_date = models.DateTimeField(default=None, blank=True)
    date = models.DateTimeField(auto_now_add=True)