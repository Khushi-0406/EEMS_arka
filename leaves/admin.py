from django.contrib import admin
from .models import LeaveType, LeaveBalance, LeaveRequest


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'total_days', 'carry_forward_allowed')
    search_fields = ('name',)


@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'leave_type', 'remaining_days')
    list_filter = ('leave_type',)
    search_fields = ('employee__username',)


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'employee', 'leave_type',
        'start_date', 'end_date',
        'status', 'approved_by'
    )
    list_filter = ('status', 'leave_type')
    search_fields = ('employee__username',)