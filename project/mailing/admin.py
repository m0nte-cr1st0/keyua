# Django imports
from django.contrib import admin

# Project imports
from project.mailing.models import *


class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = ('target', 'subject', 'name', 'event')
    list_filter = ('event', )


class MessageNotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'message', 'read')


class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'text', 'nda')


admin.site.register(EmailNotification, EmailNotificationAdmin)
admin.site.register(MessageNotification, MessageNotificationAdmin)
admin.site.register(ContactForm, ContactFormAdmin)
