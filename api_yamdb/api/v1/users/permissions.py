from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Authenticated admin or superuser only."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.is_superuser or request.user.is_admin)
        )
