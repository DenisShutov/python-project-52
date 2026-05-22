from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Label

# Create your tests here.

User = get_user_model()


class LabelTest(TestCase):
    fixtures = ['labels.json', 'tasks.json', 'statuses.json', 'users.json',]

    def setUp(self):
        self.client = Client()
        # Создаём пользователя для тестов
        self.user = User.objects.create_user(
            username='user',
            password='123'
        )
        self.client.force_login(self.user)

    def test_label_list_read(self):
        url = reverse('labels_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Фича')
        self.assertContains(response, 'Баг')

    def test_label_update(self):
        update_url = reverse('labels_update', kwargs={"pk": 1})
        list_url = reverse('labels_list')

        self.client.post(update_url, data={"name": "Улучшение"})

        response = self.client.get(list_url)
        
        self.assertContains(response, "Улучшение")
        self.assertNotContains(response, "Баг")

    def test_labels_create(self):
        create_url = reverse('labels_create')
        list_url = reverse('labels_list')

        response = self.client.post(create_url, data={'name': 'Изучение'})
        
        self.assertRedirects(response, list_url)

        label = Label.objects.get(name='Изучение')
        self.assertEqual(label.name, 'Изучение')

        response = self.client.get(list_url)
        self.assertContains(response, 'Изучение')

    def test_label_delete_protected(self):
        label = Label.objects.get(pk=1)
        self.assertTrue(label.task_set.exists())

        delete_url = reverse('labels_delete', kwargs={"pk": label.pk})
        list_url = reverse("labels_list")

        response = self.client.post(delete_url)
        self.assertRedirects(response, list_url)

        self.assertTrue(Label.objects.filter(pk=label.pk).exists())
    
    def test_label_delete_success(self):
        label = Label.objects.create(name='Временная метка')

        delete_url = reverse('labels_delete', kwargs={"pk": label.pk})
        list_url = reverse("labels_list")

        response = self.client.post(delete_url)
        self.assertRedirects(response, list_url)

        self.assertFalse(Label.objects.filter(pk=label.pk).exists())