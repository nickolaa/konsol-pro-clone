from django.db import models
from users.models import User



class TaskTemplate(models.Model):
    """Шаблон задания для быстрого создания"""
    name = models.CharField(max_length=200, verbose_name='Название шаблона')
    title = models.CharField(max_length=200, verbose_name='Заголовок задания')
    description = models.TextField(verbose_name='Описание')
    default_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_templates')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'task_templates'
        verbose_name = 'Шаблон задания'
        verbose_name_plural = 'Шаблоны заданий'
    
    def __str__(self):
        return self.name

class Task(models.Model):
    """Модель задания для самозанятого"""
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('in_progress', 'В работе'),
        ('completed', 'Выполнено'),
        ('cancelled', 'Отменено'),
                ('draft', 'Черновик'),
    ]
    
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    freelancer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_t
        template = models.ForeignKey(TaskTemplate, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')asks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'tasks'
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.title} - {self.employer}'

    def publish(self):
        """Опубликовать задание"""
        if self.status == 'draft':
            self.status = 'new'
            self.save()
            return True
        return False
    
    def can_be_published(self):
        """Проверка возможности публикации"""
        return self.status == 'draft' and self.title and self.description and self.amount


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
