import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from model_bakery import baker

from apps.tasks.filters import TaskFilter
from apps.tasks.models import Task


@pytest.mark.django_db
class TestTaskFilter:

    def test_filter_by_title(self):
        user = baker.make(User)
        task1 = baker.make(Task, title="Test Task 1", owner=user)
        task2 = baker.make(Task, title="Another Task", owner=user)

        filterset = TaskFilter({"title": "Test"}, queryset=Task.objects.all())
        assert task1 in filterset.qs
        assert task2 not in filterset.qs

    def test_filter_by_status(self):
        user = baker.make(User)
        task1 = baker.make(Task, status="PENDING", owner=user)
        task2 = baker.make(Task, status="COMPLETED", owner=user)

        filterset = TaskFilter({"status": "PENDING"}, queryset=Task.objects.all())
        assert task1 in filterset.qs
        assert task2 not in filterset.qs

    def test_filter_by_due_date_range(self):
        user = baker.make(User)
        task1 = baker.make(Task, due_date=timezone.now().date(), owner=user)
        task2 = baker.make(
            Task,
            due_date=timezone.now().date() + timezone.timedelta(days=10),
            owner=user,
        )

        filterset = TaskFilter(
            {
                "due_date_min": timezone.now().date(),
                "due_date_max": timezone.now().date() + timezone.timedelta(days=5),
            },
            queryset=Task.objects.all(),
        )
        assert task1 in filterset.qs
        assert task2 not in filterset.qs

    def test_filter_by_shared_with(self):
        user1 = baker.make(User)
        user2 = baker.make(User)
        task1 = baker.make(Task, owner=user1)
        task1.shared_with.add(user2)
        task2 = baker.make(Task, owner=user1)

        filterset = TaskFilter({"shared_with": user2.id})

        assert task1 in filterset.qs
        assert task2 not in filterset.qs

    def test_filter_by_description(self):
        user = baker.make(User)
        task1 = baker.make(Task, description="This is a test task", owner=user)
        task2 = baker.make(Task, description="Another description", owner=user)

        filterset = TaskFilter({"description": "test"}, queryset=Task.objects.all())
        assert task1 in filterset.qs
        assert task2 not in filterset.qs
