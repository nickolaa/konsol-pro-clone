from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import Task, TaskTemplate, Document, Payment
from .serializers import (
    TaskListSerializer,
    TaskDetailSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TaskTemplateSerializer,
    DocumentSerializer,
    PaymentSerializer
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
    
    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.all()
        
        # Фильтруем по ролям
        if user.is_employer:
            queryset = queryset.filter(employer=user)
        elif user.is_freelancer:
            queryset = queryset.filter(Q(freelancer=user) | Q(freelancer__isnull=True, status='new'))
        
        # Фильтры из query params
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.select_related('employer', 'freelancer', 'template')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializer
        elif self.action == 'create':
            return TaskCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TaskUpdateSerializer
        return TaskDetailSerializer
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """
        Опубликовать задание (перевести из draft в new)
        """
        task = self.get_object()
        
        # Проверяем, что пользователь - владелец задания
        if task.employer != request.user:
            return Response(
                {'error': 'Вы не можете опубликовать чужое задание'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if not task.can_be_published():
            return Response(
                {'error': 'Задание не может быть опубликовано. Проверьте все обязательные поля.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if task.publish():
            serializer = TaskDetailSerializer(task)
            return Response(serializer.data)
        
        return Response(
            {'error': 'Не удалось опубликовать задание'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """
        Назначить фрилансера на задание
        """
        task = self.get_object()
        
        if not request.user.is_freelancer:
            return Response(
                {'error': 'Только фрилансеры могут брать задания'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if task.status != 'new':
            return Response(
                {'error': 'Можно взять только новые задания'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if task.freelancer:
            return Response(
                {'error': 'Задание уже назначено'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task.freelancer = request.user
        task.status = 'in_progress'
        task.save()
        
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        Завершить задание
        """
        task = self.get_object()
        
        if task.freelancer != request.user:
            return Response(
                {'error': 'Только назначенный фрилансер может завершить задание'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if task.status != 'in_progress':
            return Response(
                {'error': 'Можно завершить только задания в работе'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task.status = 'completed'
        task.save()
        
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data)


class DocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления документами
    """
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Document.objects.filter(
            Q(task__employer=self.request.user) | Q(task__freelancer=self.request.user)
        )


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра выплат
    """
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_employer:
            return Payment.objects.filter(task__employer=user)
        elif user.is_freelancer:
            return Payment.objects.filter(freelancer=user)
        return Payment.objects.none()
