from rest_framework import permissions
from .models import ROLE_SUPER_ADMIN, AdminList


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role.role in AdminList
        )

    def has_object_permission(self, request, view, obj):
        """
        Only the Owner or Admin can access the object
        """
        return request.user.role.role in AdminList or obj == request.user


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role.role == ROLE_SUPER_ADMIN
        )

    def has_object_permission(self, request, view, obj):
        """
        Only the Owner or Admin can access the object
        """
        return request.user.role.role in AdminList or obj == request.user
