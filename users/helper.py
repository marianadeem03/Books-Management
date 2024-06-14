from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'


class IsCompanyOwner(BasePermission):
    def has_permission(self, request, view):
        # Permission is allowed only if the user is authenticated
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Object-level permission to allow only the company owner to edit
        return obj.company.owner == request.user