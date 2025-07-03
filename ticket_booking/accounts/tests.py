from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.admin = User.objects.create_user(username='admin', password='adminpass', is_admin=True)

    def test_user_registration(self):
        response = self.client.post(reverse('user_register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_registration_password_mismatch(self):
        response = self.client.post(reverse('user_register'), {
            'username': 'failuser',
            'email': 'fail@example.com',
            'password1': 'abc',
            'password2': 'def',
        })
        self.assertEqual(response.status_code, 200)  # Should not redirect
        self.assertFalse(User.objects.filter(username='failuser').exists())

    def test_user_login_logout(self):
        response = self.client.post(reverse('user_login'), {
            'username': 'testuser',
            'password': 'testpass',
        })
        self.assertEqual(response.status_code, 302)
        # Now logout
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('user_logout'))
        self.assertEqual(response.status_code, 302)

    def test_invalid_user_login(self):
        response = self.client.post(reverse('user_login'), {
            'username': 'testuser',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 200)  # Should not redirect

    def test_user_dashboard_access(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('user_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome')

    def test_admin_registration(self):
        response = self.client.post(reverse('admin_register'), {
            'username': 'admin2',
            'email': 'admin2@example.com',
            'password1': 'adminpass2',
            'password2': 'adminpass2',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='admin2').exists())

    def test_admin_login_logout(self):
        response = self.client.post(reverse('admin_login'), {
            'username': 'admin',
            'password': 'adminpass',
        })
        self.assertEqual(response.status_code, 302)
        # Now logout
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('admin_logout'))
        self.assertEqual(response.status_code, 302)

    def test_admin_dashboard_access(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin Dashboard')

    def test_user_cannot_access_admin_dashboard(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertNotEqual(response.status_code, 200)

    def test_admin_cannot_access_user_dashboard(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('user_dashboard'))
        self.assertNotEqual(response.status_code, 200)
