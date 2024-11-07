from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "category"
        ordering = ["name"]


class Task(BaseModel):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks"
    )
    shared_with = models.ManyToManyField(User, blank=True, related_name="shared_tasks")

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def mark_as_completed(self):
        if self.status == "COMPLETED":
            raise ValidationError("Task is already completed")
        self.status = "COMPLETED"
        self.updated_at = datetime.now()
        self.save()

    class Meta:
        db_table = "task"
        ordering = ["-created_at"]
