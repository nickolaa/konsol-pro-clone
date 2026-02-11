# -*- coding: utf-8 -*-
"""
Тесты для модуля отзывов (Reviews)
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from backend.models import Task, Review

User = get_user_model()

class ReviewAPITest(APITestCase):
    """Тесты API отзывов"""
    def setUp(self):
        self.client = APIClient()
        self.employer = User.objects.create_user(
            email='employer@example.com',
            password='pass',
            is_employer=True
        )
        self.freelancer = User.objects.create_user(
            email='freelancer@example.com',
            password='pass',
            is_freelancer=True
        )
        # Создаем завершенное задание
        self.task = Task.objects.create(
            title='Completed Task',
            description='Description',
            amount=5000,
            employer=self.employer,
            freelancer=self.freelancer,
            status='completed'
        )
        self.list_url = reverse('review-list')
        self.client.force_authenticate(user=self.employer)

    def test_create_review_api(self):
        """Тест создания отзыва через API"""
        data = {
            'task': self.task.id,
            'rating': 5,
            'comment': 'Excellent work!'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        
        review = Review.objects.first()
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.freelancer, self.freelancer)

    def test_cannot_review_incomplete_task(self):
        """Тест: нельзя оставить отзыв на незавершенное задание"""
        task2 = Task.objects.create(
            title='In Progress Task',
            employer=self.employer,
            freelancer=self.freelancer,
            amount=1000,
            status='in_progress'
        )
        data = {
            'task': task2.id,
            'rating': 4
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_only_employer_can_review(self):
        """Тест: только работодатель может оставить отзыв"""
        self.client.force_authenticate(user=self.freelancer)
        data = {
            'task': self.task.id,
            'rating': 5
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
