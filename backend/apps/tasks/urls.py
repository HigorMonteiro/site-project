from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, TaskViewSet

router = routers.DefaultRouter()

router.register(r"tasks", TaskViewSet, basename="task")
router.register(r"categories", CategoryViewSet, basename="category")

urlpatterns = [
    path("", include(router.urls)),
]
