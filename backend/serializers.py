from rest_framework import serializers
from .models import Task, TaskTemplate, Document, Payment, Transaction, Review
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'telegram_id', 'is_freelancer', 'is_employer']
        read_only_fields = ['id']

class TaskTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTemplate
        fields = ['id', 'name', 'title', 'description', 'default_amount', 'employer', 'created_at']
        read_only_fields = ['id', 'employer', 'created_at']
    
    def create(self, validated_data):
        validated_data['employer'] = self.context['request'].user
        return super().create(validated_data)

class TaskListSerializer(serializers.ModelSerializer):
    employer = UserSerializer(read_only=True)
    freelancer = UserSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'employer', 'freelancer', 'amount', 'status', 'status_display', 
                 'created_at', 'updated_at', 'deadline']
        read_only_fields = ['id', 'created_at', 'updated_at']

class TaskDetailSerializer(serializers.ModelSerializer):
    employer = UserSerializer(read_only=True)
    freelancer = UserSerializer(read_only=True)
    template = TaskTemplateSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    can_be_published = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'employer', 'freelancer', 'template', 'title', 'description', 'amount', 
                 'status', 'status_display', 'created_at', 'updated_at', 'deadline', 'can_be_published']
        read_only_fields = ['id', 'employer', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['employer'] = self.context['request'].user
        return super().create(validated_data)

class TaskCreateSerializer(serializers.ModelSerializer):
    template_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'template_id', 'title', 'description', 'amount', 'freelancer', 'deadline']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        template_id = validated_data.pop('template_id', None)
        validated_data['employer'] = self.context['request'].user
        
        # Если указан шаблон, заполнить данные из него
        if template_id:
            try:
                template = TaskTemplate.objects.get(
                    id=template_id, 
                    employer=self.context['request'].user
                )
                validated_data['template'] = template
                if not validated_data.get('title'):
                    validated_data['title'] = template.title
                if not validated_data.get('description'):
                    validated_data['description'] = template.description
                if not validated_data.get('amount') and template.default_amount:
                    validated_data['amount'] = template.default_amount
            except TaskTemplate.DoesNotExist:
                pass
        
        return super().create(validated_data)

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'amount', 'freelancer', 'deadline', 'status']
    
    def validate_status(self, value):
        # Можно менять статус только с draft на new через publish
        if self.instance.status == 'draft' and value != 'draft':
            if value != 'new':
                raise serializers.ValidationError('Черновик можно только опубликовать')
        return value

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'task', 'doc_type', 'file', 'created_at']
        read_only_fields = ['id', 'created_at']

class PaymentSerializer(serializers.ModelSerializer):
    task = TaskListSerializer(read_only=True)
    freelancer = UserSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'task', 'freelancer', 'amount', 'status', 'status_display', 
                 'created_at', 'processed_at']
        read_only_fields = ['id', 'created_at', 'processed_at']Add ReviewSerializer for task feedback and freelancer rating

class TransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    transaction_type_display = serializers.CharField(source='get_transaction_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'transaction_type', 'transaction_type_display', 'amount', 
                 'status', 'status_display', 'description', 'task', 'created_at', 'processed_at']
        read_only_fields = ['id', 'user', 'created_at', 'processed_at']

class ReviewSerializer(serializers.ModelSerializer):
    employer = UserSerializer(read_only=True)
    freelancer = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'task', 'employer', 'freelancer', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'employer', 'created_at']
        
    def create(self, validated_data):
        validated_data['employer'] = self.context['request'].user
        # Также автоматически заполняем freelancer из задания
        task = validated_data.get('task')
        if task:
            validated_data['freelancer'] = task.freelancer
        return super().create(validated_data)
