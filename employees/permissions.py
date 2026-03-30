from rest_framework.permissions import BasePermission


class IsHRorAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        # User must be logged in
        if not user.is_authenticated:
            return False

        # Only HR or Admin allowed
        return user.role in ['HR', 'Admin']
