from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery import baker
from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer


@pytest.mark.django_db
class TestTaskViewSetPagination:

    @pytest.fixture
    def api_client(self, user):
        client = APIClient()
        client.force_authenticate(user=user)
        return client

    def test_list_pagination_with_custom(self, api_client, user):
        tasks = baker.make(Task, user=user, _quantity=15)
        url = reverse('task-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

        expected = {
            "count": 15,
            "page_size": 2,
            "next": "http://testserver/api/tasks/?page=2",
            "previous": None,
            'results': TaskSerializer(tasks[:2], many=True).data
        }

        assert response.data["count"] == expected["count"]
        assert response.data["previous"] == expected["previous"]