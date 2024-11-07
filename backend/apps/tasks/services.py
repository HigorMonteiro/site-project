from apps.tasks.models import Task


def create_task(
    user, title, description=None, due_date=None, category=None, shared_with=None
):

    task = Task.objects.create(
        title=title,
        description=description,
        due_date=due_date,
        user=user,
        category=category,
    )

    if shared_with:
        task.shared_with.set(shared_with)

    return task
