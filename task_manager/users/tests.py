from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UserTest(TestCase):
    fixtures = ["users.json"]

    def test_update_user(self):
        user = User.objects.get(pk=3)
        # логиним без пароля
        self.client.force_login(user)

        update_url = reverse("users_update", kwargs={"pk": user.pk})
        list_url = reverse("users_list")

        self.client.post(update_url, data={"first_name": "Bob",
                                           "last_name": "Sincler",
                                           "username": "BobS"
                                           })

        response = self.client.get(list_url)
        self.assertContains(response, "Bob")
        self.assertNotContains(response, "qwdqwd")
    
    def test_delete_user(self):
        user = User.objects.get(pk=4)
        self.client.force_login(user)

        delete_url = reverse("users_delete", kwargs={"pk": user.pk})
        response = self.client.post(delete_url)

        list_url = reverse("users_list")
        self.assertRedirects(response, list_url)

        self.assertFalse(User.objects.filter(pk=4).exists())
    
    def test_delete_user_no_login(self):
        user = User.objects.get(pk=4)

        delete_url = reverse("users_delete", kwargs={"pk": user.pk})
        response = self.client.post(delete_url)

        list_url = reverse("users_list")
        self.assertRedirects(response, list_url)

        self.assertTrue(User.objects.filter(pk=4).exists())
    
    def test_user_creation(self):
        new_user = User.objects.create_user(
            first_name="Alice",
            last_name="Stranger",
            username="AliceS",
            password="123"
        )

        self.assertEqual(new_user.first_name, "Alice")
        self.assertEqual(new_user.last_name, "Stranger")
        self.assertEqual(new_user.username, "AliceS")