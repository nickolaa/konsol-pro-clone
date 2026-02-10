from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone', 'is_freelancer', 'is_employer', 'is_active']
    list_filter = ['is_freelancer', 'is_employer', 'is_active']
    search_fields = ['username', 'email', 'phone']
