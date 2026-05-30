from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from task_manager.users.forms import UserCreateForm, UserUpdateForm


class UsersListView(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(
            request,
            'users/list.html',
            context={
                'users': users
            }
        )


class UserCreateView(View):
    def get(self, request, *args, **kwargs):
        form = UserCreateForm()
        return render(request, "users/create.html", {"form": form})
    
    def post(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно зарегистрирован')
            return redirect('login')
        return render(request, "users/create.html", {"form": form})


class UserEditView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(pk=user_id)
        if user != request.user:
            messages.error(request, 'У вас нет прав для изменения')
            return redirect('users_list')
        form = UserUpdateForm(instance=user)
        return render(
            request,
            'users/update.html',
            {'form': form, 'user_id': user_id}
        )
    
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = get_object_or_404(User, pk=user_id)
        if user != request.user:
            messages.error(request, 'У вас нет прав для изменения')
            return redirect('users_list')
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно изменен')
            return redirect('users_list')
        
        return render(
            request,
            'users/update.html',
            {'form': form, 'user_id': user_id}
        )
    

class UserDeleteView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(pk=user_id)
        return render(
            request,
            'users/delete.html',
            {'user': user}
        )
    
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = get_object_or_404(User, pk=user_id)
        if user != request.user:
            messages.error(request, 'У вас нет прав для изменения')
            return redirect('users_list')
        user.delete()
        messages.success(request, 'Пользователь успешно удален')
        return redirect('users_list')

