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


class IsAdminOrSeller(BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        -> admins can use all methods
        -> users can access the view but cannot use database changing methods unless they are the sellers
        """

        if request.user.is_superuser:
            return True

        if request.method in SAFE_METHODS:
            return True

        return request.user == obj.seller
