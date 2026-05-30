from django.forms import ModelForm

from .models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['executor'].label_from_instance = (
            lambda obj: f'{obj.first_name} {obj.last_name}'
        )