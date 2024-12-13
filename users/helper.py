from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
)
from users.models import Company


class IsAdminOrCompanyOwner(BasePermission):
    """
       Custom permission to grant different levels of access based on user authentication and role.
       - Authenticated users with the role 'admin' have full access.
       - Authenticated users with company owner can read and update only.
       - Authenticated users with no company return permission denied error message.
    """

    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            if user.role == 'admin':
                return True
            elif Company.objects.filter(owner=user).exists():
                return (request.method in SAFE_METHODS
                        or request.method == 'PATCH')
            else:
                raise PermissionDenied(
                    detail="You are not authorized to perform this "
                           "action, You are not any company owner."
                )
        return False


class IsCompanyOwner(BasePermission):
    """
       Custom permission to grant different levels of access based on user authentication and role.
       - Authenticated users with the role 'admin' or company owner have full access.
       - Authenticated users with other roles can read only.
       """

    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            if Company.objects.filter(owner=user).exists() or user.role == 'admin':
                return True
            elif (
                request.method == 'POST' or
                request.method == 'PUT' or
                request.method == 'DELETE'
            ):
                raise PermissionDenied(
                    detail="You are not authorized to perform this "
                           "action, You are not any company owner."
                )
            else:
                return request.method in SAFE_METHODS
        return False


class IsAdminOrUser(BasePermission):
    """
    Custom permission to grant different levels of access based on user authentication and role.
    - Unauthenticated users have read-only access.
    - Authenticated users with the role 'admin' have full access.
    - Authenticated users with other roles can read only.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return request.method in SAFE_METHODS
        if user.role == 'admin':
            return True
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


def filter_queryset_by_user_role(model, user):
    queryset = model.objects.all()
    if Company.objects.filter(owner=user).exists():
        return queryset.filter(company__owner=user)
    if user.role == 'admin' or user.role == 'viewer':
        return queryset
    elif user.role == 'author':
        return queryset.filter(authors=user)
    elif user.role == 'publisher':
        return queryset.filter(publisher=user)
    else:
        return queryset.none()


def filter_queryset_by_company_role(model, user):
    queryset = model.objects.all()
    if user.role == 'admin':
        return queryset
    else:
        return queryset.filter(owner=user)
