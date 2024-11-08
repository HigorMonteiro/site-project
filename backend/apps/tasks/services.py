from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from apps.tasks.models import Task


class TaskService:
    @staticmethod
    def create_task(
        user,
        title,
        description=None,
        due_date=None,
        category=None,
        shared_with=None,
        status=None,
    ):
        if shared_with and user in shared_with:
            raise ValidationError("You cannot share a task with yourself.")

        try:
            with transaction.atomic():
                task = Task.objects.create(
                    title=title,
                    description=description,
                    due_date=due_date,
                    user=user,
                    category=category,
                )

                if shared_with:
                    shared_with = [u for u in shared_with if u != user]
                    task.shared_with.set(shared_with)

                return task
        except IntegrityError as e:
            raise ValidationError(f"An error occurred while creating the task: {e}")
        except Exception as e:
            raise ValidationError(f"An unexpected error occurred: {e}")

    @staticmethod
    def update_task(task_id, **kwargs):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise ValidationError("Task does not exist.")

        shared_with = kwargs.pop("shared_with", None)
        for key, value in kwargs.items():
            setattr(task, key, value)

        task.save()

        if shared_with is not None:
            task.shared_with.set(shared_with)

        return task

    @staticmethod
    def delete_task(task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise ValidationError("Task does not exist.")

        task.delete()

    @staticmethod
    def list_tasks(user):
        return Task.objects.filter(user=user)
