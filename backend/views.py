from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .pdf_generator import PDFGenerator

from .models import (
    Task, TaskTemplate, Document, Payment, Contract, Act, 
    Signature, Transaction, Review
)
from .serializers import (
    TaskListSerializer,
    TaskDetailSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TaskTemplateSerializer,
    DocumentSerializer,
    PaymentSerializer,
    TransactionSerializer,
    ReviewSerializer
)

class TaskTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления шаблонами заданий
    """
    serializer_class = TaskTemplateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Показываем только шаблоны текущего работодателя
        return TaskTemplate.objects.filter(employer=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet для полного CRUD управления заданиями
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializer
        if self.action == 'create':
            return TaskCreateSerializer
        if self.action in ['update', 'partial_update']:
            return TaskUpdateSerializer
        return TaskDetailSerializer

    def get_queryset(self):
        user = self.request.user
        # Работодатель видит свои созданные задания
        # Исполнитель видит задания, где он назначен
        # Новые задания видят все исполнители
        if user.is_employer:
            return Task.objects.filter(employer=user)
        else:
            return Task.objects.filter(Q(freelancer=user) | Q(status='new'))

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Опубликовать задание (перевести из черновика в новое)"""
        task = self.get_object()
        if task.employer != request.user:
            return Response({'error': 'Только автор может опубликовать задание'}, status=status.HTTP_403_FORBIDDEN)
        
        if task.publish():
            return Response({'status': 'Задание опубликовано'})
        return Response({'error': 'Нельзя опубликовать это задание'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """Взять задание в работу (для исполнителя)"""
        task = self.get_object()
        if not request.user.is_freelancer:
            return Response({'error': 'Только исполнители могут брать задания'}, status=status.HTTP_403_FORBIDDEN)
        
        if task.status != 'new':
            return Response({'error': 'Задание уже занято или недоступно'}, status=status.HTTP_400_BAD_REQUEST)
        
        task.freelancer = request.user
        task.status = 'in_progress'
        task.save()
        return Response({'status': 'Вы назначены исполнителем'})

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Завершить выполнение задания (для исполнителя)"""
        task = self.get_object()
        if task.freelancer != request.user:
            return Response({'error': 'Вы не являетесь исполнителем этого задания'}, status=status.HTTP_403_FORBIDDEN)
        
        if task.status != 'in_progress':
            return Response({'error': 'Задание должно быть в работе'}, status=status.HTTP_400_BAD_REQUEST)
        
        task.status = 'completed'
        task.save()
        return Response({'status': 'Задание отмечено как выполненное'})

class DocumentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Просмотр документов по заданиям
    """
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Document.objects.filter(Q(task__employer=user) | Q(task__freelancer=user))

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Просмотр выплат
    """
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_employer:
            return Payment.objects.filter(task__employer=user)
        return Payment.objects.filter(freelancer=user)

class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    История транзакций пользователя
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet для отзывов о работе исполнителей
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Работодатель видит свои данные отзывы
        # Исполнитель видит полученные отзывы
        user = self.request.user
        return Review.objects.filter(Q(employer=user) | Q(freelancer=user))

    def perform_create(self, serializer):
        # Проверяем, что задание завершено и автор - текущий пользователь
        task = serializer.validated_data.get('task')
        if task.status != 'completed':
            raise serializers.ValidationError("Отзыв можно оставить только после завершения задания")
        if task.employer != self.request.user:
            raise serializers.ValidationError("Только работодатель может оставить отзыв")
        serializer.save()
