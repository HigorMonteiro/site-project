# tasks/management/commands/populate_db.py

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from apps.tasks.models import Task
import random
from faker import Faker


class Command(BaseCommand):
    help = "Populates the database with sample data"

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        numbers = range(1, 100)
        fake = Faker()

        for _ in numbers:
            user = random.choice(users)
            Task.objects.create(
            title=fake.sentence(),
            description=fake.paragraph(),
            owner=user,
            )
        tasks = Task.objects.all()
        for task in tasks:
            task.shared_with.set(users[2:])
            task.save()
        self.stdout.write(
            self.style.SUCCESS("Successfully populated the database with sample data")
        )
