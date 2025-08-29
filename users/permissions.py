from rest_framework.permissions import BasePermission


class OwnerOrManagerPerm(BasePermission):
    """ Разрешения на обновление. """
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user == view.get_object().owner


class OwnerOnlyPerm(BasePermission):
    """ Разрешения на обновление. """
    def has_permission(self, request, view):
        return request.user == view.get_object().owner
