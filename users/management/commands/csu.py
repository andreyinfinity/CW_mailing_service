from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Create superuser"""
    def handle(self, *args, **options):
        user = User.objects.create(
            email='aapot@ya.ru',
            first_name='admin',
            is_staff=True,
            is_superuser=True,
        )
        user.set_password('0000')
        user.save()
