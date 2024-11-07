from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, TaskViewSet

router = routers.DefaultRouter()

router.register(r"tasks", TaskViewSet, basename="tasks")
router.register(r"categories", CategoryViewSet, basename="categories")

urlpatterns = [
    path("", include(router.urls)),
]
