from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Admin'


class IsHR(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'HR'


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Employee'


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Manager'