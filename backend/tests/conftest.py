import pytest
from django.contrib.auth.models import User
from model_bakery import baker

from apps.tasks.models import Category, Task


@pytest.fixture
def user(db):
    return baker.make(User)


@pytest.fixture
def category(user, db):
    return baker.make(Category, owner=user)


@pytest.fixture
def task(user, db):
    return baker.make(Task, owner=user)
