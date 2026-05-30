from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Label, Status, Task

# Create your tests here.

User = get_user_model()


class TaskTest(TestCase):
    fixtures = ['tasks.json', 'statuses.json', 'users.json', 'labels.json']

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
        label = Label.objects.first()

        update_url = reverse('tasks_update', kwargs={"pk": 2})
        list_url = reverse('tasks_list')

        self.client.post(update_url, data={
        "name": "blabla2",
        "description": "новое описание",
        "status": 3,
        "executor": 4,
        "labels": [label.pk] if label else [],
    })

        response = self.client.get(list_url)
        
        self.assertContains(response, "blabla2")
        self.assertNotContains(response, "Blbla1")

    def test_task_create(self):
        create_url = reverse('tasks_create')
        list_url = reverse('tasks_list')

        label = Label.objects.first()

        response = self.client.post(create_url, data={
            "name": "Новая задача",
            "description": "Описание новой задачи",
            "status": 3,
            "executor": 4,
            "labels": [label.pk] if label else [],
        })

        self.assertRedirects(response, list_url)
        self.assertTrue(Task.objects.filter(name="Новая задача").exists())
        
        response = self.client.get(list_url)
        self.assertContains(response, "Новая задача")
    
    def test_task_delete(self):
        status = Status.objects.first()
        task = Task.objects.create(
            name='Задача для удаления',
            description='Описание',
            status=status,
            author=self.user,
            executor=self.user
        )

        delete_url = reverse('tasks_delete', kwargs={"pk": task.pk})
        list_url = reverse('tasks_list')

        response = self.client.post(delete_url)
        self.assertRedirects(response, list_url)
        
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())

    def test_task_delete_protected(self):
        task = Task.objects.exclude(author=self.user).first()
        
        self.assertIsNotNone(task)
        self.assertNotEqual(task.author, self.user)

        delete_url = reverse('tasks_delete', kwargs={"pk": task.pk})
        list_url = reverse('tasks_list')

        response = self.client.post(delete_url)
        self.assertRedirects(response, list_url)

        self.assertTrue(Task.objects.filter(pk=task.pk).exists())