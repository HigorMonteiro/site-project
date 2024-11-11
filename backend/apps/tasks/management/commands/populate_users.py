from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Populates the database with sample users"

    def handle(self, *args, **kwargs):
        # Create active users
        User.objects.create_superuser(username="pedro", email="pedro@gmail.com", password="asdf1234")
        User.objects.create_superuser(username="ze", email="ze@gmail.com", password="asdf1234")
        User.objects.create_superuser(username="maria", email="maria@gmail.com", password="asdf1234")
        User.objects.create_superuser(username="admin", email="admin@gmail.com", password="asdf1234")
        self.stdout.write(
            self.style.SUCCESS("Successfully populated the database with sample users")
        )
