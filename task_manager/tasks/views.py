from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django_filters.views import FilterView

from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task

# Create your views here.


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter
    
    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['request'] = self.request
        return kwargs


class TaskView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = get_object_or_404(Task, pk=task_id)
        return render(
            request,
            'tasks/view.html',
            context={
                'task': task
            }
        )


class TaskCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, "tasks/create.html", {"form": form})
    
    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)  
            task.author = request.user 
            task.save()
            messages.success(request, 'Задача успешно создана')
            return redirect('tasks_list')
        return render(request, "tasks/create.html", {"form": form})
    

class TaskEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = Task.objects.get(pk=task_id)
        
        form = TaskForm(instance=task)
        return render(
            request,
            'tasks/update.html',
            {'form': form, 'task_id': task_id}
        )
    
    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = get_object_or_404(Task, pk=task_id)
        
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача успешно изменена')
            return redirect('tasks_list')
        
        return render(
            request,
            'tasks/update.html',
            {'form': form, 'task_id': task_id}
        )


class TaskDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = Task.objects.get(pk=task_id)
        if task.author != request.user:
            messages.error(request, 'Задачу может удалить только ее автор')
            return redirect('tasks_list')
        return render(
            request,
            'tasks/delete.html',
            {'task': task}
        )
    
    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = get_object_or_404(Task, pk=task_id)
        if task.author != request.user:
            messages.error(request, 'Задачу может удалить только ее автор')
            return redirect('tasks_list')
        
        task.delete()
        messages.success(request, 'Задача успешно удалена')
        return redirect('tasks_list')