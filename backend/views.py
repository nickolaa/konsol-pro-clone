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
    serializer_class = TaskTemplateSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return TaskTemplate.objects.filter(employer=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        if self.action == 'list': return TaskListSerializer
        if self.action == 'create': return TaskCreateSerializer
        if self.action in ['update', 'partial_update']: return TaskUpdateSerializer
        return TaskDetailSerializer
    def get_queryset(self):
        user = self.request.user
        if user.is_employer: return Task.objects.filter(employer=user)
        return Task.objects.filter(Q(freelancer=user) | Q(status='new'))

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        task = self.get_object()
        if task.employer != request.user: return Response({'error': '403'}, status=status.HTTP_403_FORBIDDEN)
        if task.publish(): return Response({'status': 'published'})
        return Response({'error': '400'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        task = self.get_object()
        if not request.user.is_freelancer: return Response({'error': '403'}, status=status.HTTP_403_FORBIDDEN)
        if task.status != 'new': return Response({'error': 'taken'}, status=status.HTTP_400_BAD_REQUEST)
        task.freelancer = request.user
        task.status = 'in_progress'
        task.save()
        return Response({'status': 'assigned'})

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        if task.freelancer != request.user: return Response({'error': '403'}, status=status.HTTP_403_FORBIDDEN)
        if task.status != 'in_progress': return Response({'error': '400'}, status=status.HTTP_400_BAD_REQUEST)
        task.status = 'completed'
        task.save()
        return Response({'status': 'completed'})

    @action(detail=True, methods=['post'])
    def generate_contract(self, request, pk=None):
        task = self.get_object()
        if task.employer != request.user or hasattr(task, 'contract') or not task.freelancer:
            return Response({'error': 'invalid'}, status=status.HTTP_400_BAD_REQUEST)
        from datetime import date, timedelta
        contract = Contract.objects.create(
            task=task, contract_number=f'C-{task.id}', employer=task.employer,
            freelancer=task.freelancer, contract_date=date.today(),
            work_description=task.description, amount=task.amount,
            deadline=date.today() + timedelta(days=7)
        )
        pdf_gen = PDFGenerator()
        contract.pdf_file = pdf_gen.generate_contract(contract)
        contract.status = 'pending_signature'
        contract.save()
        return Response({'status': 'generated'})
          @action(detail=True, methods=['post'])
    def generate_act(self, request, pk=None):
        task = self.get_object()
        if task.employer != request.user or hasattr(task, 'act') or task.status != 'completed':
            return Response({'error': 'invalid'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not hasattr(task, 'contract') or task.contract.status != 'signed':
            return Response({'error': 'contract not signed'}, status=status.HTTP_400_BAD_REQUEST)

        from datetime import date
        act = Act.objects.create(
            task=task,
            contract=task.contract,
            act_number=f'A-{task.id}',
            act_date=date.today(),
            work_performed=task.description,
            amount=task.amount
        )
        pdf_gen = PDFGenerator()
        act.pdf_file = pdf_gen.generate_act(act)
        act.status = 'pending_signature'
        act.save()
        return Response({'status': 'generated'})

    @action(detail=True, methods=['post'])
    def sign_contract(self, request, pk=None):
        task = self.get_object()
        if not hasattr(task, 'contract'):
            return Response({'error': 'no contract'}, status=status.HTTP_400_BAD_REQUEST)
        
        contract = task.contract
        if contract.status != 'pending_signature':
            return Response({'error': 'invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        Signature.objects.create(
            user=request.user,
            document_type='contract',
            document_id=contract.id,
            signature_data=f"Signed by {request.user.email} at {date.today()}",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        contract.status = 'signed'
        contract.save()
        return Response({'status': 'signed'})

    @action(detail=True, methods=['post'])
    def sign_act(self, request, pk=None):
        task = self.get_object()
        if not hasattr(task, 'act'):
            return Response({'error': 'no act'}, status=status.HTTP_400_BAD_REQUEST)
        
        act = task.act
        if act.status != 'pending_signature':
            return Response({'error': 'invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        Signature.objects.create(
            user=request.user,
            document_type='act',
            document_id=act.id,
            signature_data=f"Signed by {request.user.email} at {date.today()}",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        act.status = 'signed'
        act.save()
        
        Payment.objects.create(
            task=task,
            freelancer=task.freelancer,
            amount=task.amount,
            status='pending'
        )
        
        return Response({'status': 'signed'})


class DocumentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Document.objects.filter(Q(task__employer=user) | Q(task__freelancer=user))

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.is_employer: return Payment.objects.filter(task__employer=user)
        return Payment.objects.filter(freelancer=user)

class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(Q(employer=user) | Q(freelancer=user))
    def perform_create(self, serializer):
        task = serializer.validated_data.get('task')
        if task.status != 'completed' or task.employer != self.request.user:
            raise serializers.ValidationError(\"Invalid task or user\")
        serializer.save()
