from django.urls import path
from task_manager.tasks import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='tasks_list'),
]