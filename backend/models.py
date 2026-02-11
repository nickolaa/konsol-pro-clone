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



class Contract(models.Model):
    """Модель договора"""
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('pending_signature', 'Ожидает подписи'),
        ('signed', 'Подписан'),
        ('cancelled', 'Отменен'),
    ]
    
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='contract')
    contract_number = models.CharField(max_length=50, unique=True)
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employer_contracts')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='freelancer_contracts')
    
    # Данные для заполнения шаблона
    contract_date = models.DateField()
    work_description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    
    # PDF файл
    pdf_file = models.FileField(upload_to='contracts/', null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'contracts'
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Договор №{self.contract_number}'
    
    def generate_contract_number(self):
        """Генерирует номер договора"""
        from datetime import datetime
        return f'C-{datetime.now().strftime("%Y%m%d")}-{self.id}'


class Act(models.Model):
    """Модель акта выполненных работ"""
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('pending_signature', 'Ожидает подписи'),
        ('signed', 'Подписан'),
        ('cancelled', 'Отменен'),
    ]
    
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='act')
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='acts')
    act_number = models.CharField(max_length=50, unique=True)
    
    # Данные для заполнения шаблона
    act_date = models.DateField()
    work_performed = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # PDF файл
    pdf_file = models.FileField(upload_to='acts/', null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'acts'
        verbose_name = 'Акт'
        verbose_name_plural = 'Акты'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Акт №{self.act_number}'
    
    def generate_act_number(self):
        """Генерирует номер акта"""
        from datetime import datetime
        return f'A-{datetime.now().strftime("%Y%m%d")}-{self.id}'


class Signature(models.Model):
    """Модель подписи (ПЭП)"""
    DOCUMENT_TYPE_CHOICES = [
        ('contract', 'Договор'),
        ('act', 'Акт'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='signatures')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    document_id = models.IntegerField()
    
    # Данные подписи
    signature_data = models.TextField(help_text='Данные электронной подписи')
    signed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        db_table = 'signatures'
        verbose_name = 'Подпись'
        verbose_name_plural = 'Подписи'
        ordering = ['-signed_at']
        # Один пользователь может подписать документ только один раз
        unique_together = [['user', 'document_type', 'document_id']]
    
    def __str__(self):
        return f'Подпись {self.user} - {self.document_type} #{self.document_id}'


class Transaction(models.Model):
    """Модель транзакций для пополнения баланса и выплат"""
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Пополнение'),
        ('payout', 'Выплата'),
        ('payment', 'Оплата задания'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'В обработке'),
        ('completed', 'Завершена'),
        ('failed', 'Отклонена'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    description = models.TextField(blank=True)
    task = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'transactions'
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.get_transaction_type_display()} - {self.amount} руб. ({self.user.email})'
