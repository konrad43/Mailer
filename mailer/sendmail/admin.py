from django.contrib import admin

from .models import Mailbox, Template
admin.site.register(Mailbox)
admin.site.register(Template)
