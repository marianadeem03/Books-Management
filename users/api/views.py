from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from users.models import (
    Book,
    Company,
    BookFeedback,
)
from users.api.serializers import (
    BookSerializer,
    AdminCompanySerializer,
    BookFeedbackSerializer,
)
from users.helper import (
    IsAdminOrUser,
    IsCompanyOwner,
    IsAdminOrCompanyOwner,
    filter_queryset_by_user_role,
    filter_queryset_by_company_role,
)


class AdminCompanyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrCompanyOwner]
    serializer_class = AdminCompanySerializer
    queryset = Company.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'owner__username', ]

    def get_queryset(self):
        return filter_queryset_by_company_role(Company, self.request.user)


class BooksViewSet(viewsets.ModelViewSet):
    permission_classes = [IsCompanyOwner]
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'rating', ]
    filterset_fields = ['company__id', ]

    def get_queryset(self):
        return filter_queryset_by_user_role(Book, self.request.user)


class BookFeedbackViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrUser]
    serializer_class = BookFeedbackSerializer
    queryset = BookFeedback.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['book__title', 'rating', ]

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
