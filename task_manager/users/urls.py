from django.urls import path
from task_manager.users import views

urlpatterns = [
    path('', views.UsersListView.as_view(), name='users_list'),
    path('create/', views.UserCreateView.as_view(), name='users_create'),
    path('<int:id>/update/', views.UserEditView.as_view(), name='users_update'),
    path('<int:id>/delete/', views.UserDeleteView.as_view(), name='users_delete'),
]
