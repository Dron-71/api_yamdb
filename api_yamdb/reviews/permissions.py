from rest_framework import permissions

class IsAllowedOrReadOnly(permissions.BasePermission):
    """
    Anonymous: can only read,
    Authenticated: can add new titles, reviews and comments,
    Administrator: can read, write all records,
    Moderator: can read, write and delete all records,
    Superuser: can do everything possible
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif (request.method not in permissions.SAFE_METHODS
              and request.user.is_authenticated
              or request.user.is_superuser):
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif (request.method in ('PATCH', 'DELETE')
              and (request.user.is_moderator or request.user.is_admin)
                or request.user == obj.author):
            return True
        else:
            return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """Администратор или только чтение"""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_superuser or request.user.is_admin)))
