import pytest
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.forms import ValidationError
from model_bakery import baker

from apps.tasks.models import Category, Task


@pytest.mark.django_db
class TestCategoryModel:

    def test_category_creation(self, user):
        category = baker.make(Category, user=user)
        assert Category.objects.count() == 1
        assert str(category) == category.name

    def test_category_unique_name(self, user):
        baker.make(Category, name="Category 1", user=user)
        with pytest.raises(IntegrityError):
            baker.make(Category, name="Category 1", user=user)


@pytest.mark.django_db
class TestTaskModel:
    def test_task_creation(self, user):
        task = baker.make(Task, user=user)
        assert Task.objects.count() == 1
        assert str(task) == f"{task.title} - {user.username}"

    def test_mark_as_completed(self, task):
        initial_updated_at = task.updated_at

        task.mark_as_completed()
        assert task.status == "COMPLETED"
        assert task.updated_at > initial_updated_at

    def test_already_completed_raises_error(self, user):
        task = baker.make(Task, status="COMPLETED", user=user)

        with pytest.raises(ValidationError):
            task.mark_as_completed()

    def test_start(self):
        user = baker.make(User, username="test")
        task = baker.make(Task, user=user)
        assert task.status == "PENDING"
