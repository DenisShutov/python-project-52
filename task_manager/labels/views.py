from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from task_manager.labels.models import Label
from task_manager.labels.forms import LabelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# Create your views here.
class LabelListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        labels = Label.objects.all()
        return render(
            request,
            'labels/list.html',
            context={
                'labels': labels
            }
        )

class LabelCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = LabelForm()
        return render(request, "labels/create.html", {"form": form})
    
    def post(self, request, *args, **kwargs):
        form = LabelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Метка успешно создана')
            return redirect('labels_list')
        return render(request, "labels/create.html", {"form": form})

class LabelEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        label = Label.objects.get(pk=label_id)
        
        form = LabelForm(instance=label)
        return render(
            request,
            'labels/update.html',
            {'form': form, 'label_id': label_id}
        )
    
    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        label = get_object_or_404(Label, pk=label_id)
        
        form = LabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.success(request, 'Метка успешно изменена')
            return redirect('labels_list')
        
        return render(
            request,
            'labels/update.html',
            {'form': form, 'label_id': label_id}
        )

class LabelDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        label = Label.objects.get(pk=label_id)
        return render(
            request,
            'labels/delete.html',
            {'label': label}
        )
    
    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        label = get_object_or_404(Label, pk=label_id)
        
        label.delete()
        messages.success(request, 'Метка успешно удалена')
        return redirect('labels_list')