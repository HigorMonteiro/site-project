import datetime

from django.forms import ValidationError
import pytest
from django.contrib.auth.models import User
from apps.tasks.models import Task
from model_bakery import baker

from apps.tasks.services import create_task


@pytest.mark.django_db
class TestServices:
    def test_create_task_service(self, user, category):

        shared_users = baker.make(User, _quantity=3)

        due_date = datetime.date(2024, 5, 10)

        task = create_task(
            user,
            "Service Task",
            due_date=due_date,
            description="New task",
            category=category,
            shared_with=shared_users,
        )
        assert task.title == "Service Task"
        assert task.description == "New task"
        assert task.category == category
        assert task.due_date == due_date
        for shared_user in shared_users:
            assert shared_user in task.shared_with.all()

        assert len(task.shared_with.all()) == len(shared_users)

    def test_create_task_service_with_self(self, user, category):
        with pytest.raises(ValidationError, match="You cannot share a task with yourself."):
            create_task(
                user,
                "Service Task",
                description="New task",
                category=category,
                shared_with=[user],
            )
        assert Task.objects.count() == 0

    def test_create_task_service_with_self_in_shared(self, user, category):
        with pytest.raises(ValidationError, match="You cannot share a task with yourself."):
            create_task(
                user,
                "Service Task",
                description="New task",
                category=category,
                shared_with=[user, baker.make(User)],
            )
        assert Task.objects.count() == 0
