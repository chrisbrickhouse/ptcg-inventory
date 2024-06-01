from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            password = os.environ.get('CARDSITE_SYSOP_PASSWORD')
            if password is None:
                raise ValueError("Password not found")
            User.objects.create_superuser(
                username='admin',
                email='',
                password=password
            )
