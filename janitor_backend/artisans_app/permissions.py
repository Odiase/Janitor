from rest_framework.permissions import BasePermission


class IsArtisan(BasePermission):
    """
    Custom permission to only allow artisans to access certain views.
    """

    def has_permission(self, request, view):
        try:
            return bool(request.user and request.user.is_authenticated and request.user.artisan_profile.is_artisan)
        except AttributeError:
            return False
