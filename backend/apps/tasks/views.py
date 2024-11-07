from django.contrib.auth.models import User
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .models import Category, Task
from .serializers import CategorySerializer, TaskSerializer
from .services import create_task


class TaskViewSet(viewsets.ModelViewSet):

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        queryset = Task.objects.filter(user=self.request.user).order_by().distinct()
        shared_tasks = self.request.user.shared_tasks.all().order_by().distinct()
        queryset = queryset.union(shared_tasks)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        title = serializer.validated_data["title"]
        description = serializer.validated_data.get("description")
        due_date = serializer.validated_data.get("due_date")
        category_id = serializer.validated_data.get("category")

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"detail": "Category not found"}, status=400)

        shared_with_ids = request.data.get("shared_with", [])
        try:

            shared_with = User.objects.filter(id__in=shared_with_ids)
        except User.DoesNotExist:

            return Response({"detail": "User not found"}, status=400)

        task = create_task(user, title, description, due_date, category, shared_with)
        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        title = serializer.validated_data.get("title", instance.title)
        description = serializer.validated_data.get("description", instance.description)
        due_date = serializer.validated_data.get("due_date", instance.due_date)
        status = serializer.validated_data.get("status", instance.status)

        category_id = serializer.validated_data.get("category")
        if category_id:
            category = Category.objects.get(pk=category_id)
            instance.category = category

        shared_with_ids = request.data.get("shared_with", [])

        if shared_with_ids:
            shared_with_users = User.objects.filter(pk__in=shared_with_ids)
            instance.shared_with.set(shared_with_users)

        if title:
            instance.title = title

        if description:
            instance.description = description
        if due_date:
            instance.due_date = due_date

        if status:
            instance.status = status

        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.user != self.request.user:

            return Response(status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        if instance.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
