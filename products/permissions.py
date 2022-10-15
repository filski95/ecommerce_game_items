from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        """
        -> admins can use all methods
        -> users can access the view but cannot use database changing methods
        """
        if not request.user.is_superuser:
            if request.method in SAFE_METHODS:
                return True
            return False
        return True
