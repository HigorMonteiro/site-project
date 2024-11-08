import django_filters
from django.contrib.auth.models import User

from .models import Task


class TaskFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(lookup_expr="icontains")
    description = django_filters.CharFilter(lookup_expr="icontains")

    status = django_filters.ChoiceFilter(choices=Task.STATUS_CHOICES)

    due_date = django_filters.DateFilter()
    due_date_min = django_filters.DateFilter(field_name="due_date", lookup_expr="gte")
    due_date_max = django_filters.DateFilter(field_name="due_date", lookup_expr="lte")

    category = django_filters.CharFilter(
        field_name="category__name", lookup_expr="icontains"
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.filters["shared_with"].queryset = User.objects.filter(id=self.user.id)

    shared_with = django_filters.CharFilter(
        field_name="shared_with",
    )

    class Meta:
        model = Task
        fields = [
            "title",
            "status",
            "due_date",
            "due_date_min",
            "due_date_max",
            "shared_with",
            "description",
            "category",
        ]
