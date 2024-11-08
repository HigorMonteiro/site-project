from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Populates the database with sample users"

    def handle(self, *args, **kwargs):
        # Create active users
        User.objects.create_user(username="pedro", password="asdf1234", is_active=True)
        User.objects.create_user(username="ze", password="asdf1234", is_active=True)
        User.objects.create_user(username="maria", password="asdf1234")

        # Create superusers
        User.objects.create_superuser(
            username="higor", password="asdf1234", is_active=True
        )
        User.objects.create_superuser(
            username="bia", password="asdf1234", is_active=True
        )

        # Random users
        User.objects.create_user(username="ana", password="asdf1234", is_active=True)
        User.objects.create_user(username="joao", password="asdf1234", is_active=True)
        User.objects.create_user(username="jose", password="asdf1234", is_active=True)
        User.objects.create_user(username="lucas", password="asdf1234", is_active=True)
        User.objects.create_user(username="lais", password="asdf1234", is_active=True)
        User.objects.create_user(username="livia", password="asdf1234", is_active=True)
        User.objects.create_user(username="lucia", password="asdf1234", is_active=True)

        self.stdout.write(
            self.style.SUCCESS("Successfully populated the database with sample users")
        )
