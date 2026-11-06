from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient


class UserApiSecurityTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        user_model = get_user_model()

        self.admin = user_model.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='Admin12345',
        )
        self.user = user_model.objects.create_user(
            username='maria',
            email='maria@test.com',
            password='Clave12345',
            telefono='6620000000',
        )
        self.client.force_authenticate(user=self.admin)

    def test_password_never_appears_in_users_response(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('password', response.data[0])

    def test_partial_update_without_password_keeps_current_password(self):
        current_hash = self.user.password
        response = self.client.patch(
            f'/api/v1/users/{self.user.id}/',
            {'first_name': 'Maria Elena'},
            format='json',
        )
        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()
        self.assertEqual(self.user.password, current_hash)
        self.assertTrue(self.user.check_password('Clave12345'))

    def test_partial_update_with_password_changes_password(self):
        response = self.client.patch(
            f'/api/v1/users/{self.user.id}/',
            {'password': 'NuevaClave123'},
            format='json',
        )
        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NuevaClave123'))


class UserProfileEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username='ana',
            email='ana@test.com',
            password='Ana12345',
            telefono='6621111111',
        )
        self.client.force_authenticate(user=self.user)

    def test_auth_me_does_not_return_password(self):
        response = self.client.get('/api/v1/auth/me/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('password', response.data)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['telefono'], self.user.telefono)

    def test_login_with_email_returns_jwt_tokens(self):
        client = APIClient()
        response = client.post(
            '/api/token/',
            {'email': self.user.email, 'password': 'Ana12345'},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
