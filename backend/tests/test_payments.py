# -*- coding: utf-8 -*-
"""
Тесты для модуля платежей и выплат (Payments)
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from decimal import Decimal
from payments.models import Transaction, Wallet

User = get_user_model()


class PaymentModelTest(TestCase):
    """Тесты моделей платежей"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='payer@example.com',
            password='pass'
        )
        self.wallet, _ = Wallet.objects.get_or_create(user=self.user)

    def test_wallet_creation(self):
        """Тест создания кошелька при создании пользователя"""
        self.assertEqual(self.wallet.balance, Decimal('0.00'))

    def test_transaction_creation(self):
        """Тест создания транзакции"""
        tx = Transaction.objects.create(
            user=self.user,
            amount=Decimal('1000.00'),
            transaction_type='deposit',
            status='completed',
            description='Test deposit'
        )
        self.assertEqual(tx.amount, Decimal('1000.00'))
        self.assertEqual(tx.status, 'completed')


class PaymentAPITest(APITestCase):
    """Тесты API платежей"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='finance@example.com',
            password='pass'
        )
        self.client.force_authenticate(user=self.user)
        self.transactions_url = reverse('transaction-list')
        self.deposit_url = reverse('transaction-deposit')
        self.payout_url = reverse('transaction-payout')
        self.balance_url = reverse('user-balance')

    def test_get_transactions_history(self):
        """Тест получения истории транзакций"""
        Transaction.objects.create(user=self.user, amount=500, transaction_type='deposit')
        Transaction.objects.create(user=self.user, amount=200, transaction_type='payout')
        
        response = self.client.get(self.transactions_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_deposit_api(self):
        """Тест пополнения баланса через API"""
        data = {'amount': 5000, 'method': 'card'}
        response = self.client.post(self.deposit_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.filter(transaction_type='deposit').count(), 1)

    def test_payout_request_api(self):
        """Тест запроса выплаты"""
        # Сначала пополним баланс
        wallet = Wallet.objects.get(user=self.user)
        wallet.balance = Decimal('10000.00')
        wallet.save()
        
        data = {'amount': 3000, 'method': 'bank'}
        response = self.client.post(self.payout_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.filter(transaction_type='payout').count(), 1)

    def test_payout_insufficient_funds(self):
        """Тест выплаты при недостаточном балансе"""
        data = {'amount': 1000000}
        response = self.client.post(self.payout_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_current_balance(self):
        """Тест получения текущего баланса"""
        wallet = Wallet.objects.get(user=self.user)
        wallet.balance = Decimal('750.50')
        wallet.save()
        
        response = self.client.get(self.balance_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data['balance']), Decimal('750.50'))
