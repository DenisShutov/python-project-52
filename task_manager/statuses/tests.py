from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Status
# Create your tests here.

User = get_user_model()

class StatusTest(TestCase):
    fixtures = ['statuses.json']

    def setUp(self):
        self.client = Client()
        # Создаём пользователя для тестов
        self.user = User.objects.create_user(
            username='user',
            password='123'
        )
        self.client.force_login(self.user)

    def test_status_read(self):
        url = reverse('statuses_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'На рассмотрении')
        self.assertContains(response, 'В работе')

    def test_status_update(self):
        update_url = reverse('statuses_update', kwargs={"pk": 3})
        list_url = reverse('statuses_list')

        self.client.post(update_url, data={"name": "Выполнено"})

        response = self.client.get(list_url)
        
        self.assertContains(response, "Выполнено")
        self.assertNotContains(response, "В работе")

    def test_status_create(self):
        create_url = reverse('statuses_create')
        list_url = reverse('statuses_list')

        response = self.client.post(create_url, data={'name': 'Изучается'})
        
        self.assertRedirects(response, list_url)

        status = Status.objects.get(name='Изучается')
        self.assertEqual(status.name, 'Изучается')

        response = self.client.get(list_url)
        self.assertContains(response, 'Изучается')

    def test_status_delete(self):

        delete_url = reverse('statuses_delete', kwargs={"pk": 3})
        list_url = reverse("statuses_list")

        response = self.client.post(delete_url)
        self.assertRedirects(response, list_url)

        self.assertFalse(Status.objects.filter(pk=3).exists())