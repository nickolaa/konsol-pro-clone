from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'telegram_id', 'is_freelancer', 'is_employer']
        read_only_fields = ['id']
