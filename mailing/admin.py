from django.contrib import admin

from mailing.models import Mail, Mailing


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'body', 'user']
    list_filter = ['user']


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    list_filter = ['user']
    ordering = ['user', '-create_date']
