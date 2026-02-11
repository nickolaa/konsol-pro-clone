from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from users.models import User
from .models import Task, TaskTemplate, Document, Payment, Contract, Act, ContractTemplate, Signature, Transaction, Review


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """Расширенная админ-панель для пользователей"""
    list_display = ['email', 'phone', 'is_freelancer', 'is_employer', 'is_active', 'date_joined']
    list_filter = ['is_freelancer', 'is_employer', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['email', 'phone', 'telegram_id']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {'fields': ('phone', 'telegram_id')}),
        ('Роли', {'fields': ('is_freelancer', 'is_employer')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_freelancer', 'is_employer'),
        }),
    )
    
    actions = ['activate_users', 'deactivate_users']
    
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f'Активировано пользователей: {queryset.count()}')
    activate_users.short_description = 'Активировать выбранных пользователей'
    
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f'Деактивировано пользователей: {queryset.count()}')
    deactivate_users.short_description = 'Деактивировать выбранных пользователей'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Расширенная админ-панель для заданий с модерацией"""
    list_display = ['title', 'employer', 'freelancer', 'amount', 'status_badge', 'created_at']
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['title', 'description', 'employer__email', 'freelancer__email']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'amount', 'deadline')
        }),
        ('Участники', {
            'fields': ('employer', 'freelancer')
        }),
        ('Статус', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )
    
    actions = ['approve_tasks', 'reject_tasks', 'mark_in_progress', 'mark_completed']
    
    def status_badge(self, obj):
        colors = {
            'draft': 'gray',
            'published': 'blue',
            'in_progress': 'orange',
            'completed': 'green',
            'cancelled': 'red',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Статус'
    
    def approve_tasks(self, request, queryset):
        queryset.filter(status='draft').update(status='published')
        self.message_user(request, f'Одобрено заданий: {queryset.count()}')
    approve_tasks.short_description = 'Одобрить задания (опубликовать)'
    
    def reject_tasks(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, f'Отклонено заданий: {queryset.count()}')
    reject_tasks.short_description = 'Отклонить задания'
    
    def mark_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
        self.message_user(request, f'Переведено в работу: {queryset.count()}')
    mark_in_progress.short_description = 'Перевести в работу'
    
    def mark_completed(self, request, queryset):
        queryset.update(status='completed')
        self.message_user(request, f'Завершено заданий: {queryset.count()}')
    mark_completed.short_description = 'Завершить задания'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Админ-панель для управления транзакциями и выплатами"""
    list_display = ['id', 'user', 'transaction_type_badge', 'amount', 'status_badge', 'created_at']
    list_filter = ['transaction_type', 'status', 'created_at']
    search_fields = ['user__email', 'description']
    readonly_fields = ['created_at', 'processed_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Информация о транзакции', {
            'fields': ('user', 'transaction_type', 'amount', 'description')
        }),
        ('Статус и связи', {
            'fields': ('status', 'task', 'created_at', 'processed_at')
        }),
    )
    
    actions = ['approve_transactions', 'reject_transactions']
    
    def transaction_type_badge(self, obj):
        colors = {
            'deposit': 'green',
            'payout': 'orange',
            'payment': 'blue',
        }
        color = colors.get(obj.transaction_type, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, obj.get_transaction_type_display()
        )
    transaction_type_badge.short_description = 'Тип'
    
    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'completed': 'green',
            'failed': 'red',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Статус'
    
    def approve_transactions(self, request, queryset):
        from django.utils import timezone
        queryset.filter(status='pending').update(status='completed', processed_at=timezone.now())
        self.message_user(request, f'Одобрено транзакций: {queryset.count()}')
    approve_transactions.short_description = 'Одобрить транзакции'
    
    def reject_transactions(self, request, queryset):
        from django.utils import timezone
        queryset.filter(status='pending').update(status='failed', processed_at=timezone.now())
        self.message_user(request, f'Отклонено транзакций: {queryset.count()}')
    reject_transactions.short_description = 'Отклонить транзакции'


@admin.register(TaskTemplate)
class TaskTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'employer', 'default_amount', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'title', 'description']
    readonly_fields = ['created_at']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['task', 'doc_type', 'created_at']
    list_filter = ['doc_type', 'created_at']
    search_fields = ['task__title']
    readonly_fields = ['created_at']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['task', 'freelancer', 'amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['task__title', 'freelancer__email']
    readonly_fields = ['created_at', 'processed_at']


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['task', 'created_at']
    list_filter = ['created_at']
    search_fields = ['task__title']
    readonly_fields = ['created_at']


@admin.register(Act)
class ActAdmin(admin.ModelAdmin):
    list_display = ['task', 'created_at']
    list_filter = ['created_at']
    search_fields = ['task__title']
    readonly_fields = ['created_at']


@admin.register(ContractTemplate)
class ContractTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']


@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
    list_display = ['user', 'document_type', 'created_at']
    list_filter = ['document_type', 'created_at']

    @admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['task', 'employer', 'freelancer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['task__title', 'employer__email', 'freelancer__email', 'comment']
    readonly_fields = ['created_at']
    search_fields = ['user__email']
