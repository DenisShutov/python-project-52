import django_filters

from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label='Метка'
    )
    
    my_tasks = django_filters.BooleanFilter(
        method='filter_my_tasks',
        label='Только свои задачи',
    )
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def filter_my_tasks(self, queryset, name, value):
        if value and hasattr(self, 'request'):
            return queryset.filter(author=self.request.user)
        return queryset
    
    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']