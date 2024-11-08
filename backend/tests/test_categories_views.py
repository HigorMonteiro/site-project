import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from model_bakery import baker
from django.contrib.auth.models import User
from apps.tasks.models import Category


@pytest.mark.django_db
class TestCategoryViewSet:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    def test_create_category(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse('category-list')
        data = {
            "name": "New Category",
            "user": user.id
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.count() == 1
        assert Category.objects.get().name == "New Category"

    def test_create_category_invalid_data(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse('category-list')
        data = {}
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Category.objects.count() == 0

    def test_update_category(self, api_client, user, category):
        api_client.force_authenticate(user=user)
        url = reverse('category-detail', args=[category.id])
        data = {
            "name": "Updated Category",
            "user": user.id
        }
        response = api_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        category.refresh_from_db()
        assert category.name == "Updated Category"

    def test_update_category_does_not_exist(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse('category-detail', args=[999])
        data = {
            "name": "Updated Category"
        }
        response = api_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_category(self, api_client, user, category):
        api_client.force_authenticate(user=user)
        url = reverse('category-detail', args=[category.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Category.objects.count() == 0

    def test_delete_category_user_forbidden(self, api_client, user):
        category = baker.make(Category, user=baker.make(User))
        api_client.force_authenticate(user=user)
        url = reverse('category-detail', args=[category.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND    

    def test_list_categories(self, api_client, user, category):
        api_client.force_authenticate(user=user)
        url = reverse('category-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]['name'] == category.name