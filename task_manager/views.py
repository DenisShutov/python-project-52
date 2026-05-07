from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from task_manager.forms import UserCreateForm, UserUpdateForm, UserLoginForm
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def index(request):
    return render(
        request,
        'index.html',
        context={
            'message': 'Hello'
        },
    )

class UsersListView(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(
            request,
            'users.html',
            context={
                'users': users
            }
        )

class UserCreateView(View):
    def get(self, request, *args, **kwargs):
        form = UserCreateForm()
        return render(request, "users_create.html", {"form": form})
    
    def post(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно зарегистрирован')
            return redirect('index')
        return render(request, "users_create.html", {"form": form})


class UserEditView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        if user != request.user:
            messages.error(request, 'У вас нет прав для изменения')
            return redirect('users')
        form = UserUpdateForm(instance=user)
        return render(
            request,
            'users_update.html',
            {'form': form, 'user_id': user_id}
        )
    
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = get_object_or_404(User, id=user_id)
        if user != request.user:
            messages.error(request, 'У вас нет прав для изменения')
            return redirect('users')
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно изменен')
            return redirect('login')
        
        return render(
            request,
            'users_update.html',
            {'form': form, 'user_id': user_id}
        )
    
class UserDeleteView(View):
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = get_object_or_404(User, id=user_id)
        if user != request.user:
            messages.error(request, 'У вас нет прав для изменения')
            return redirect('users')
        user.delete()
        messages.success(request, 'Пользователь успешно удален')
        return redirect('users')

class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render (
            request,
            'users_login.html',
            {'form': form}
        )
    
    def post(self, request):
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
        
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы залогинены')
                return redirect('index')
        
        return render (
            request,
            'users_login.html',
            {'form': form}
        )

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'Вы разлогинены')
        return redirect('index')