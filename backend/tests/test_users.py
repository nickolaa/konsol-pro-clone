# -*- coding: utf-8 -*-
"""
Тесты для модели пользователя и аутентификации
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta

User = get_user_model()


class UserModelTest(TestCase):
    """Тесты модели User"""

    def setUp(self):
        """"Настройка тестовых данных"""
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Иван',
            'last_name': 'Петров',
            'phone': '+79001234567'
        }

    def test_create_user(self):
        """Тест создания пользователя"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        """Тест создания суперпользователя"""
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='admin123'
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)

    def test_user_str_method(self):
        """Тест строкового представления"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data['email'])

    def test_user_roles(self):
        """Тест ролей пользователя"""
        # Создаем заказчика
        employer = User.objects.create_user(
            email='employer@example.com',
            password='test123',
            is_employer=True
        )
        self.assertTrue(employer.is_employer)
        self.assertFalse(employer.is_freelancer)

        # Создаем исполнителя
        freelancer = User.objects.create_user(
            email='freelancer@example.com',
            password='test123',
            is_freelancer=True
        )
        self.assertTrue(freelancer.is_freelancer)
        self.assertFalse(freelancer.is_employer)


class AuthenticationAPITest(APITestCase):
    """Тесты API аутентификации"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.client = APIClient()
        self.register_url = reverse('auth:register')
        self.login_url = reverse('auth:login')
        self.profile_url = reverse('auth:profile')
        
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'StrongPass123!',
            'first_name': 'Test',
            'last_name': 'User',
            'is_employer': True
        }

    def test_user_registration(self):
        """Тест регистрации пользователя"""
        response = self.client.post(self.register_url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, self.user_data['email'])

    def test_user_registration_duplicate_email(self):
        """Тест регистрации с существующим email"""
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.register_url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        """Тест входа пользователя"""
        User.objects.create_user(**self.user_data)
        
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_wrong_credentials(self):
        """Тест входа с неверными данными"""
        User.objects.create_user(**self.user_data)
        
        wrong_login_data = {
            'email': self.user_data['email'],
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, wrong_login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_profile_authenticated(self):
        """Тест получения профиля аутентифицированным пользователем"""
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)
        
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user_data['email'])

    def test_get_user_profile_unauthenticated(self):
        """Тест получения профиля без аутентификации"""
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_profile(self):
        """Тест обновления профиля"""
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)
        
        update_data = {
            'first_name': 'Updated',
            'phone': '+79999999999'
        }
        response = self.client.patch(self.profile_url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Updated')
        self.assertEqual(user.phone, '+79999999999')


class JWTTokenTest(APITestCase):
    """Тесты JWT токенов"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='testtoken@example.com',
            password='testpass123'
        )
        self.refresh_url = reverse('token_refresh')

    def test_token_generation(self):
        """Тест генерации токенов"""
        refresh = RefreshToken.for_user(self.user)
        
        self.assertIsNotNone(str(refresh))
        self.assertIsNotNone(str(refresh.access_token))

    def test_token_refresh(self):
        """Тест обновления токена"""
        refresh = RefreshToken.for_user(self.user)
        
        response = self.client.post(
            self.refresh_url,
            {'refresh': str(refresh)},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
