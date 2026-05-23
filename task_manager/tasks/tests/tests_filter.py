from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Label, Status

# Create your tests here.

User = get_user_model()


class TaskFilterTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.first()
        self.client.force_login(self.user)
    
    def test_filter_by_status(self):
        status = Status.objects.first()
        url = reverse('tasks_list')
        response = self.client.get(url, {'status': status.id})
        
        self.assertEqual(response.status_code, 200)
    
    def test_filter_by_executor(self):
        executor = User.objects.last()
        url = reverse('tasks_list')
        response = self.client.get(url, {'executor': executor.id})
        
        self.assertEqual(response.status_code, 200)
    
    def test_filter_by_label(self):
        label = Label.objects.first()
        url = reverse('tasks_list')
        response = self.client.get(url, {'labels': label.id})
        
        self.assertEqual(response.status_code, 200)
    
    def test_filter_my_tasks(self):
        url = reverse('tasks_list')
        response = self.client.get(url, {'my_tasks': 'on'})
        
        self.assertEqual(response.status_code, 200)