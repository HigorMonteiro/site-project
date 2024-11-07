from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Category, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "created_at", "user")


class TaskSerializer(serializers.ModelSerializer):

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False, allow_null=True
    )
    shared_with = UserSerializer(many=True, required=False)

    class Meta:

        model = Task
        fields = (
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "due_date",
            "status",
            "user",
            "category",
            "shared_with",
        )
        read_only_fields = ("id", "created_at", "updated_at", "user")
