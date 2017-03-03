from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(email="admin@silohq.com").exists():
            User.objects.create_superuser("admin", "admin@silohq.com", "R4d2Yp+Mgf4!>Dy%")
