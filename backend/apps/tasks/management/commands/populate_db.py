# tasks/management/commands/populate_db.py

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from apps.tasks.models import Task


class Command(BaseCommand):
    help = "Populates the database with sample data"

    def handle(self, *args, **kwargs):
        users = User.objects.all()

        for user in users:
            Task.objects.create(
                title=f"Task-{user}", description="Description", owner=user
            )

        tasks = Task.objects.all()
        for task in tasks:
            task.shared_with.set(users[1:])
            task.save()
        self.stdout.write(
            self.style.SUCCESS("Successfully populated the database with sample data")
        )
