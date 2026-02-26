from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'role', 'is_verified', 'is_active']
    list_filter = ['role', 'is_verified', 'is_active', 'is_staff']
    search_fields = ['email', 'username', 'first_name', 'last_name', 'student_id']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone_number', 'department', 'student_id', 'profile_picture', 'is_verified')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'role', 'phone_number', 'department', 'student_id')
        }),
    )
