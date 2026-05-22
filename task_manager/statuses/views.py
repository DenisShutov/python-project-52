from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


# Create your views here.
class StatusListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        return render(
            request,
            'statuses/list.html',
            context={
                'statuses': statuses
            }
        )


class StatusCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = StatusForm()
        return render(request, "statuses/create.html", {"form": form})
    
    def post(self, request, *args, **kwargs):
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус успешно создан')
            return redirect('statuses_list')
        return render(request, "statuses/create.html", {"form": form})


class StatusEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        status = Status.objects.get(pk=status_id)
        
        form = StatusForm(instance=status)
        return render(
            request,
            'statuses/update.html',
            {'form': form, 'status_id': status_id}
        )
    
    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        status = get_object_or_404(Status, pk=status_id)
        
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус успешно изменен')
            return redirect('statuses_list')
        
        return render(
            request,
            'statuses/update.html',
            {'form': form, 'status_id': status_id}
        )
    

class StatusDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        status = Status.objects.get(pk=status_id)
        return render(
            request,
            'statuses/delete.html',
            {'status': status}
        )
    
    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        status = get_object_or_404(Status, pk=status_id)
        
        status.delete()
        messages.success(request, 'Статус успешно удален')
        return redirect('statuses_list')