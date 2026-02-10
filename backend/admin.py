from django.contrib import admin
from .models import Task, Document, Payment


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'employer', 'freelancer', 'amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description', 'employer__telegram_id', 'freelancer__telegram_id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['task', 'doc_type', 'created_at']
    list_filter = ['doc_type', 'created_at']
    search_fields = ['task__title']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['task', 'freelancer', 'amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['task__title', 'freelancer__telegram_id']
    readonly_fields = ['created_at', 'processed_at']
