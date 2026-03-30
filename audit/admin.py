from django.contrib import admin
from .models import AuditLog, LoginActivity

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('user__username', 'action')

@admin.register(LoginActivity)
class LoginActivityAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'login_time',
        'logout_time',
        'ip_address',
        'is_active',
    )
    list_filter = ('is_active', 'login_time')
    search_fields = ('user__username', 'ip_address')