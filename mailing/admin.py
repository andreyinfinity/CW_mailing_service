from django.contrib import admin

from mailing.models import Mail, Mailing


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ['title', 'body']


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ['name']
