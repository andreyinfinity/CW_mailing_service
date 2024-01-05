from datetime import timedelta
from django.core.mail import EmailMessage
from django.core.management import BaseCommand
from django.db.models import F
from django.utils import timezone
from django.utils.datetime_safe import datetime
from config.settings import EMAIL_HOST_USER
from mailing.models import Mailing


day = timedelta(days=1, hours=0, minutes=0)
week = timedelta(days=7, hours=0, minutes=0)
month = timedelta(days=30, hours=0, minutes=0)


class Command(BaseCommand):
    """Команда для запуска рассылки"""
    def handle(self, *args, **options):
        self.start_mailing()

    def start_mailing(self):
        # установка временного статуса sending на время отправки писем
        (Mailing.objects.filter(
            status__in=['created', 'in progress'],
            next_date__lte=datetime.now(timezone.utc)).
         update(status='sending'))
        mailings = Mailing.objects.filter(status='sending')

        for mailing in mailings:
            self.send_mail(mailing)
            if mailing.period == 'onetime':
                mailing.next_date = None
                mailing.status = 'completed'
            elif mailing.period == 'daily':
                mailing.status = 'in progress'
                mailing.next_date = F('next_date') + day
            elif mailing.period == 'weekly':
                mailing.status = 'in progress'
                mailing.next_date = F('next_date') + week
            elif mailing.period == 'monthly':
                mailing.status = 'in progress'
                mailing.next_date = F('next_date') + month
            mailing.save()

    def send_mail(self, mailing):
        """Отправка письма"""
        mail_subject = mailing.mail.title
        message = mailing.mail.body
        to_email = [customer.email for customer in mailing.customers.all()]
        email = EmailMessage(subject=mail_subject, body=message, to=to_email, from_email=EMAIL_HOST_USER)
        email.send()
