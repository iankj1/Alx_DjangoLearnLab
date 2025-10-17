# posts/permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to allow owners to edit/delete only.
    """

    def has_object_permission(self, request, view, obj):
        # Read-only allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write allowed only to the object's author
        # Works for Post and Comment (both have 'author')
        return getattr(obj, "author", None) == request.user
