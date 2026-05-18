from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from task_manager.tasks.models import Task
# Create your views here.

class TaskListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        return render(
            request,
            'tasks/list.html',
            context={
                'tasks': tasks
            }
        )