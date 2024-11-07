from django.contrib import admin

from .models import Category, Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "due_date"]
    search_fields = ["title"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    search_fields = ["name"]


admin.site.register(Task, TaskAdmin)
admin.site.register(Category, CategoryAdmin)
