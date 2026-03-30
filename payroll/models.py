from django.db import models
from django.conf import settings

class Payroll(models.Model):

    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)

    basic_salary = models.FloatField()
    allowances = models.FloatField(default=0)
    deductions = models.FloatField(default=0)
    bonus = models.FloatField(default=0)

    net_salary = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.net_salary = self.basic_salary + self.allowances + self.bonus - self.deductions
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.username} - {self.month}"
