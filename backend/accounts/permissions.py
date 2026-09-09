from rest_framework.permissions import BasePermission

from .models import User


class HasRole(BasePermission):

    role = None
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.role == self.role)


class IsConsumer(HasRole):
    role = User.Role.CONSUMER
    message = "This action is only available to consumers."


class IsFarmer(HasRole):
    role = User.Role.FARMER
    message = "This action is only available to farmers."


class IsAdminRole(HasRole):

    role = User.Role.ADMIN
    message = "This action is restricted to administrators."


class IsOwner(BasePermission):

    owner_field = "user"
    message = "You do not have permission to access this resource."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        owner = getattr(obj, self.owner_field, None)
        return owner is not None and owner == request.user