from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .pdf_generator import PDFGenerator

from .models import Task, TaskTemplate, Document, Payment, Contract, Act, Signature
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



class ContractViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления договорами
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Contract.objects.filter(
            Q(employer=user) | Q(freelancer=user)
        ).select_related('task', 'employer', 'freelancer')
    
    @action(detail=True, methods=['post'])
    def generate_pdf(self, request, pk=None):
        """
        Генерирует PDF договора
        """
        contract = self.get_object()
        
        if contract.employer != request.user:
            return Response(
                {'error': 'Только заказчик может генерировать договор'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        generator = PDFGenerator()
        pdf_file = generator.generate_contract(contract)
        contract.pdf_file = pdf_file
        contract.status = 'pending_signature'
        contract.save()
        
        return Response({'message': 'PDF успешно сгенерирован', 'pdf_url': contract.pdf_file.url})
    
    @action(detail=True, methods=['post'])
    def sign(self, request, pk=None):
        """
        Подписать договор (ПЭП)
        """
        contract = self.get_object()
        
        if contract.status != 'pending_signature':
            return Response(
                {'error': 'Договор не готов к подписанию'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Проверяем права
        if request.user not in [contract.employer, contract.freelancer]:
            return Response(
                {'error': 'Вы не можете подписать этот договор'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Создаем подпись
        signature_data = request.data.get('signature_data', f'Signed by {request.user.id}')
        ip_address = request.META.get('REMOTE_ADDR')
        
        Signature.objects.create(
            user=request.user,
            document_type='contract',
            document_id=contract.id,
            signature_data=signature_data,
            ip_address=ip_address
        )
        
        # Проверяем, подписали ли обе стороны
        signatures_count = Signature.objects.filter(
            document_type='contract',
            document_id=contract.id
        ).count()
        
        if signatures_count == 2:
            contract.status = 'signed'
            contract.save()
        
        return Response({'message': 'Договор успешно подписан'})


class ActViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления актами
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Act.objects.filter(
            Q(contract__employer=user) | Q(contract__freelancer=user)
        ).select_related('task', 'contract')
    
    @action(detail=True, methods=['post'])
    def generate_pdf(self, request, pk=None):
        """
        Генерирует PDF акта
        """
        act = self.get_object()
        
        if act.contract.employer != request.user:
            return Response(
                {'error': 'Только заказчик может генерировать акт'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        generator = PDFGenerator()
        pdf_file = generator.generate_act(act)
        act.pdf_file = pdf_file
        act.status = 'pending_signature'
        act.save()
        
        return Response({'message': 'PDF успешно сгенерирован', 'pdf_url': act.pdf_file.url})
    
    @action(detail=True, methods=['post'])
    def sign(self, request, pk=None):
        """
        Подписать акт (ПЭП)
        """
        act = self.get_object()
        
        if act.status != 'pending_signature':
            return Response(
                {'error': 'Акт не готов к подписанию'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Проверяем права
        if request.user not in [act.contract.employer, act.contract.freelancer]:
            return Response(
                {'error': 'Вы не можете подписать этот акт'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Создаем подпись
        signature_data = request.data.get('signature_data', f'Signed by {request.user.id}')
        ip_address = request.META.get('REMOTE_ADDR')
        
        Signature.objects.create(
            user=request.user,
            document_type='act',
            document_id=act.id,
            signature_data=signature_data,
            ip_address=ip_address
        )
        
        # Проверяем, подписали ли обе стороны
        signatures_count = Signature.objects.filter(
            document_type='act',
            document_id=act.id
        ).count()
        
        if signatures_count == 2:
            act.status = 'signed'
            act.save()
        
        return Response({'message': 'Акт успешно подписан'})


class SignatureViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра подписей
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Signature.objects.filter(user=self.request.user)
