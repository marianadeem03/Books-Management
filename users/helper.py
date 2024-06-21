from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
)
from users.models import Company


class IsAdminOrCompanyOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == 'admin':
                return True
            elif Company.objects.filter(owner=request.user).exists():
                return request.method in SAFE_METHODS
        return False


class IsCompanyOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if (Company.objects.filter(owner=request.user).exists() or
                    request.user.role == 'admin'):
                return True
            else:
                # User is authenticated but does not own any company
                # Grant read-only permissions for safe methods
                return request.method in SAFE_METHODS
        return False


class IsAdminOrUser(BasePermission):
    """
    Custom permission to grant different levels of access based on user authentication and role.
    - Unauthenticated users have read-only access.
    - Authenticated users with the role 'admin' have full access.
    - Authenticated users with other roles can read or post only.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return request.method in SAFE_METHODS
        if request.user.role == 'admin':
            return True
        return request.method in SAFE_METHODS or request.method == 'POST'

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
