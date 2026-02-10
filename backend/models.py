from django.db import models
from users.models import User


class Task(models.Model):
    """Модель задания для самозанятого"""
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('in_progress', 'В работе'),
        ('completed', 'Выполнено'),
        ('cancelled', 'Отменено'),
    ]
    
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    freelancer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'tasks'
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.title} - {self.employer}'


class Document(models.Model):
    """Модель документа"""
    DOC_TYPE_CHOICES = [
        ('contract', 'Договор'),
        ('act', 'Акт'),
        ('invoice', 'Счет'),
    ]
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=20, choices=DOC_TYPE_CHOICES)
    file = models.FileField(upload_to='documents/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'documents'
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
    
    def __str__(self):
        return f'{self.doc_type} - {self.task}'


class Payment(models.Model):
    """Модель выплаты"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('processing', 'Обрабатывается'),
        ('completed', 'Выполнено'),
        ('failed', 'Ошибка'),
    ]
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='payments')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'payments'
        verbose_name = 'Выплата'
        verbose_name_plural = 'Выплаты'
    
    def __str__(self):
        return f'Выплата {self.amount} для {self.freelancer}'
