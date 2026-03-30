from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import EmployeeProfile, EmployeeStatusHistory, EmployeeDepartmentTransfer
from .serializers import EmployeeProfileSerializer
from .permissions import IsHRorAdmin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class EmployeeProfileViewSet(viewsets.ModelViewSet):
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsHRorAdmin]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user

        if user.role in ['HR', 'Admin']:
            return EmployeeProfile.objects.all()

        return EmployeeProfile.objects.filter(user=user)


    def perform_update(self, serializer):
        instance = self.get_object()   # old instance

        # OLD VALUES STORE KARO
        old_status = instance.status
        old_department = instance.department

        # SAVE UPDATED DATA
        updated_instance = serializer.save()

        new_status = updated_instance.status
        new_department = updated_instance.department

        # STATUS HISTORY
        if old_status != new_status:
            EmployeeStatusHistory.objects.create(
                employee=updated_instance,
                old_status=old_status,
                new_status=new_status,
                changed_by=self.request.user
            )

        # DEPARTMENT TRANSFER HISTORY
        if old_department != new_department:
            EmployeeDepartmentTransfer.objects.create(
                employee=updated_instance,
                old_department=old_department,
                new_department=new_department,
                transferred_by=self.request.user
            )


class TerminateEmployeeView(APIView):
    def post(self, request, pk):

        try:
            employee = Employee.objects.get(id=pk)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=404)

        termination_date = request.data.get("termination_date")
        reason = request.data.get("reason")

        # Update Employee
        employee.status = "TERMINATED"
        employee.is_active = False
        employee.save()

        # Create Termination Record
        EmployeeTermination.objects.create(
            employee=employee,
            termination_date=termination_date,
            reason=reason,
            terminated_by=request.user
        )

        return Response({
            "message": "Employee terminated successfully"
        })

