from django.db import IntegrityError
from django.forms import ValidationError
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from apps.tasks.services import TaskService
from model_bakery import baker
from django.contrib.auth.models import User
from apps.tasks.models import Task


@pytest.mark.django_db
class TestTaskViewSet:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    def test_create_task(self, api_client, user, category):
        api_client.force_authenticate(user=user)
        url = reverse('task-list')
        data = {
            "title": "New Task",
            "description": "Task description",
            "due_date": "2024-05-10",
            "category": category.id,
            "shared_with": []
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Task.objects.count() == 1
        assert Task.objects.get().title == "New Task"

    def test_create_task_invalid_data(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse('task-list')
        data = {
            "title": "New Task",
            "description": "Task description",
            "due_date": "2024-05-10",
            "category": 100,
            "shared_with": []
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Task.objects.count() == 0

    def test_create_task_integrity_error(self, mocker, user):
        mocker.patch('apps.tasks.models.Task.objects.create', side_effect=IntegrityError("Integrity error"))
        
        with pytest.raises(ValidationError, match="An error occurred while creating the task: Integrity error"):
            TaskService.create_task(
                user=user,
                title="New Task",
                description="Task description",
                due_date="2024-05-10",
                category=None,
                shared_with=[]
            )
            
    def test_create_task_unexpected_error(self, mocker, user):
        mocker.patch('apps.tasks.models.Task.objects.create', side_effect=Exception("Unexpected error"))
        
        with pytest.raises(ValidationError, match="An unexpected error occurred: Unexpected error"):
            TaskService.create_task(
                user=user,
                title="New Task",
                description="Task description",
                due_date="2024-05-10",
                category=None,
                shared_with=[]
            )

    def test_update_task(self, api_client, user, task):
        api_client.force_authenticate(user=user)
        url = reverse('task-detail', args=[task.id])
        data = {
            "title": "Updated Task",
            "description": "Updated description",
            "due_date": "2024-06-10",
            "category": task.category,
            "shared_with": []
        }
        response = api_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        task.refresh_from_db()
        assert task.title == "Updated Task"
        assert task.description == "Updated description"

    def test_update_task_does_not_exist(self, mocker):
        mocker.patch('apps.tasks.models.Task.objects.get', side_effect=Task.DoesNotExist)
        
        with pytest.raises(ValidationError, match="Task does not exist."):
            TaskService.update_task(task_id=1, title="Updated Task")

    def test_update_task_does_not_exist_to_user(self, api_client, user, category):
        task = baker.make(Task, user=baker.make(User), category=category)
        api_client.force_authenticate(user=user)
        url = reverse('task-detail', args=[task.id])
        data = {
            "title": "Updated Task",
            "description": "Updated description",
            "due_date": "2024-06-10",
            "category": category.id,
            "shared_with": []
        }

        response = api_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_task(self, api_client, user, task):
        api_client.force_authenticate(user=user)
        url = reverse('task-detail', args=[task.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Task.objects.count() == 0

    def test_delete_task_user_forbidden(self, api_client, user):
        task = baker.make(Task, user=baker.make(User))
        api_client.force_authenticate(user=user)
        url = reverse('task-detail', args=[task.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_task_does_not_exist(self):
        with pytest.raises(ValidationError, match="Task does not exist."):
            TaskService.delete_task(task_id=999)

    def test_list_tasks(self, user, task):
        tasks = TaskService.list_tasks(user=user)
        assert tasks.count() == 1


    def test_get_task_list(self, api_client, user, task):
        api_client.force_authenticate(user=user)
        url = reverse('task-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['title'] == task.title
