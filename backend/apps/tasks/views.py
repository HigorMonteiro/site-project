from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .filters import TaskFilter
from .models import Category, Task
from .serializers import CategorySerializer, TaskSerializer
from .services import TaskService


class TaskViewSet(viewsets.ModelViewSet):

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = TaskFilter

    def get_queryset(self):

        queryset = Task.objects.filter(user=self.request.user).order_by().distinct()
        shared_tasks = self.request.user.shared_tasks.all().order_by().distinct()
        queryset = queryset | shared_tasks
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user

        task = TaskService.create_task(user, **serializer.validated_data)
        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        task = TaskService.update_task(instance.id, **serializer.validated_data)
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        TaskService.delete_task(instance.id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
