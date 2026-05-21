from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Task
# Create your tests here.

User = get_user_model()

class TaskTest(TestCase):
    fixtures = ['tasks.json', 'statuses.json', 'users.json']

    def setUp(self):
        self.client = Client()
        # берём пользователя из фикстуры
        self.user = User.objects.first()
        self.client.force_login(self.user)
    
    def test_task_list_read(self):
        url = reverse('tasks_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Blbla1')
        self.assertContains(response, 'sdfhasf')
        self.assertContains(response, 'asfasfdasf')
    
    def test_task_update(self):
        update_url = reverse('tasks_update', kwargs={"pk": 2})
        list_url = reverse('tasks_list')

        self.client.post(update_url, data={
        "name": "blabla2",
        "description": "новое описание",
        "status": 3,
        "executor": 4,
    })

        response = self.client.get(list_url)
        
        self.assertContains(response, "blabla2")
        self.assertNotContains(response, "Blbla1")