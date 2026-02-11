# -*- coding: utf-8 -*-
"""
Тесты для модуля заданий (Tasks)
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from tasks.models import Task, TaskTemplate

User = get_user_model()


class TaskModelTest(TestCase):
    """Тесты модели Task"""

    def setUp(self):
        self.employer = User.objects.create_user(
            email='employer@example.com',
            password='pass',
            is_employer=True
        )
        self.template = TaskTemplate.objects.create(
            title='Тестовый шаблон',
            description='Описание'
        )

    def test_task_creation(self):
        """Тест создания задания"""
        task = Task.objects.create(
            title='Новое задание',
            description='Нужно сделать X',
            budget=5000,
            employer=self.employer,
            status='draft'
        )
        self.assertEqual(task.title, 'Новое задание')
        self.assertEqual(task.status, 'draft')
        self.assertEqual(task.employer, self.employer)

    def test_task_status_transitions(self):
        """Тест переходов статусов"""
        task = Task.objects.create(
            title='Задание',
            employer=self.employer,
            status='draft'
        )
        
        # Публикация
        task.status = 'published'
        task.save()
        self.assertEqual(task.status, 'published')
        
        # В работу
        task.status = 'in_progress'
        task.save()
        self.assertEqual(task.status, 'in_progress')


class TaskAPITest(APITestCase):
    """Тесты API заданий"""

    def setUp(self):
        self.client = APIClient()
        self.employer = User.objects.create_user(
            email='boss@example.com',
            password='pass',
            is_employer=True
        )
        self.freelancer = User.objects.create_user(
            email='worker@example.com',
            password='pass',
            is_freelancer=True
        )
        self.list_url = reverse('task-list')
        self.client.force_authenticate(user=self.employer)

    def test_create_task_api(self):
        """Тест создания задания через API"""
        data = {
            'title': 'API Task',
            'description': 'Description',
            'budget': 10000,
            'status': 'draft'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

    def test_get_task_list(self):
        """Тест получения списка заданий"""
        Task.objects.create(title='T1', employer=self.employer, status='published')
        Task.objects.create(title='T2', employer=self.employer, status='published')
        
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_publish_task_action(self):
        """Тест кастомного действия публикации"""
        task = Task.objects.create(title='Draft', employer=self.employer, status='draft')
        url = reverse('task-publish', args=[task.id])
        
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.status, 'published')

    def test_freelancer_cannot_create_task(self):
        """Тест: исполнитель не может создавать задания"""
        self.client.force_authenticate(user=self.freelancer)
        data = {'title': 'Fail'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
