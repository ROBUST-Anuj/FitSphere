"""
Custom DRF permissions.
"""

from rest_framework.permissions import BasePermission


class IsAuthenticatedAndActive(BasePermission):
    """
    User must be authenticated and active.
    """

    message = "Inactive account."

    def has_permission(self, request, view):

        return bool(request.user and request.user.is_authenticated and request.user.is_active)
