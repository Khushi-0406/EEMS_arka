from django.utils import timezone
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class EmployeeProfile(models.Model):

    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Terminated', 'Terminated'),
        ('On Leave', 'On Leave'),   
        ('Resigned', 'Resigned'),  
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    joining_date = models.DateField()

    reporting_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='team_members'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Active'
    )

    created_at = models.DateTimeField(auto_now_add=True)   # Added
    updated_at = models.DateTimeField(auto_now=True)       # Added

    def __str__(self):
        return self.employee_id


# NEW MODEL — Status History Tracking

class EmployeeStatusHistory(models.Model):

    employee = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.CASCADE,
        related_name='status_history'
    )

    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)

    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    reason = models.TextField(blank=True, null=True)

    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.employee_id} | {self.old_status} → {self.new_status}"


User = get_user_model()

class EmployeeDepartmentTransfer(models.Model):
    employee = models.ForeignKey(
        "EmployeeProfile",
        on_delete=models.CASCADE,
        related_name="department_transfers"
    )

    old_department = models.CharField(max_length=100)
    new_department = models.CharField(max_length=100)

    transferred_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    transferred_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.employee_id} - {self.old_department} → {self.new_department}"


class EmployeeTermination(models.Model):
    employee = models.ForeignKey('employees.EmployeeProfile', on_delete=models.CASCADE)
    termination_date = models.DateField()
    reason = models.TextField()
    terminated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.employee.employee_id.full_name + " Terminated"

