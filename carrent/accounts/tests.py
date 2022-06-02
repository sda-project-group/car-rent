from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse('users-registration')
        self.login_url = reverse('login')
        self.User = {
            'email': 'test@gmail.com',
            'username': 'username',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'birthday': '2000-01-01',
            'addr_city': 'addr_city',
            'addr_street': 'addr_street',
            'addr_post_code': '12-345',
            'mobile_nr': '123-456-789',
            'password': 'password',
            'password2': 'password',
        }

        self.user_invalid_email = {
            'email': 'gmail.com',
            'username': 'username',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'birthday': '2000-01-01',
            'addr_city': 'addr_city',
            'addr_street': 'addr_street',
            'addr_post_code': '12-345',
            'mobile_nr': '123-456-789',
            'password': 'password',
            'password2': 'password',
        }

        self.user_not_fit_password = {
            'email': 'test@gmail.com',
            'username': 'username',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'birthday': '2000-01-01',
            'addr_city': 'addr_city',
            'addr_street': 'addr_street',
            'addr_post_code': '12-345',
            'mobile_nr': '123-456-789',
            'password': 'password12',
            'password2': 'password23',
        }
        return super().setUp()


class RegisterTest(BaseTest):

    def test_can_view_page_correct(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/registration.html')

    def test_can_register_user(self):
        response = self.client.post(self.register_url, self.User, format='text/html')
        self.assertEqual(response.status_code, 200)


    def test_cant_register_user_with_not_fit_password(self):
        response = self.client.post(self.register_url, self.user_not_fit_password, format='text/html')
        self.assertEqual(response.status_code, 200)


    def test_cant_register_user_with_invalid_email(self):
        response = self.client.post(self.register_url, self.user_invalid_email, format='text/html')
        self.assertEqual(response.status_code, 200)


class LoginTest(BaseTest):
    def test_can_view_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_success(self):
        self.client.post(self.register_url, self.User, format='text/html')
        User = get_user_model().objects.filter(email=self.User['email'])
        User.is_active = True
        response = self.client.post(self.login_url, self.User, format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_cantlogin_with_no_username(self):
        response = self.client.post(self.login_url, {'password': 'password', 'username': 'abc'}, format='text/html')
        self.assertEqual(response.status_code, 200)

