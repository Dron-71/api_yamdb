from rest_framework import permissions


class IsAuthorOrStaff(permissions.IsAuthenticated):
    """Access only for author and moderator or admin."""

    def has_object_permission(self, request, view, obj):
        return bool(
            obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
            or request.user.is_superuser
        )
