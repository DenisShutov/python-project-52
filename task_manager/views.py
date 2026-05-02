from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View

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