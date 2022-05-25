from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User

# User = get_user_model()


class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse('users-registration')
        self.login_url = reverse('login')

        return super().setUp()


class LoginTest(BaseTest):
    def test_can_access_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')