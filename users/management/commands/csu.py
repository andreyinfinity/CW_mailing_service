import os
from django.core.management import BaseCommand
from dotenv import load_dotenv
from users.models import User


load_dotenv()


class Command(BaseCommand):
    """Create superuser"""
    def handle(self, *args, **options):
        user = User.objects.create(
            email=os.getenv('SUPERUSER_EMAIL'),
            first_name='admin',
            is_staff=True,
            is_superuser=True,
        )
        user.set_password(os.getenv('SUPERUSER_PASSWORD'))
        user.save()
