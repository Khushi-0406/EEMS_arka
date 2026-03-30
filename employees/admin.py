from django.contrib import admin
from .models import (
    EmployeeProfile,
    EmployeeStatusHistory,
    EmployeeDepartmentTransfer,
    EmployeeTermination
)


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "employee_id",
        "department",
        "designation",
        "status",
        "joining_date"
    )
    search_fields = ("employee_id", "department", "designation")
    list_filter = ("department", "status")


@admin.register(EmployeeStatusHistory)
class EmployeeStatusHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "old_status",
        "new_status",
        "changed_by",
        "changed_at"
    )
    list_filter = ("old_status", "new_status")


@admin.register(EmployeeDepartmentTransfer)
class EmployeeDepartmentTransferAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "old_department",
        "new_department",
        "transferred_by",
        "transferred_at"
    )
    list_filter = ("old_department", "new_department")


admin.site.register(EmployeeTermination)