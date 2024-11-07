from django.core.exceptions import ValidationError

from apps.tasks.models import Task


def create_task(
    user, title, description=None, due_date=None, category=None, shared_with=None
):

    if shared_with and user in shared_with:
        raise ValidationError("You cannot share a task with yourself.")

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
