from django.shortcuts import render, redirect
from task_manager.users.forms import UserLoginForm
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

class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render (
            request,
            'login.html',
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
            'login.html',
            {'form': form}
        )

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'Вы разлогинены')
        return redirect('index')