from rest_framework import permissions
# from rest_framework_simplejwt.authentication import JWTAuthentication


class IsAdmin(permissions.BasePermission):
    """Authenticated admin or superuser only."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.is_superuser or request.user.is_admin)
        )

    # def has_permission(self, request, view):
    #     jwt_authenticator = JWTAuthentication()
    #     response = jwt_authenticator.authenticate(request)
    #     return bool(
    #         response
    #         and (response[0].is_superuser or response[0].is_admin)
    #     )
