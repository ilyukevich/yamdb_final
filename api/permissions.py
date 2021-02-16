from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Разрешения изменений только админам остальным только чтение
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешения изменений модераторам и админам
    """
    def has_object_permission(self, request, view, obj):
        return (
            (obj.author == request.user)
            or request.method in permissions.SAFE_METHODS
            or request.user.is_moderator
            )
    