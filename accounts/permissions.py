from rest_framework import permissions


class UserOrIsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        -> Admin can see/access everything at accounts/users/[id]
        -> users can only see their details (list view not available based on get-permissions on the viewset)
        """
        user = request.user

        if user.is_superuser is True:
            return True

        return user.id == obj.id
