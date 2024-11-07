import datetime

import pytest
from django.contrib.auth.models import User
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
