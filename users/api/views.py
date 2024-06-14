from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from users.models import Book, Company
from .serializers import BookSerializer, AdminCompanySerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from users.helper import IsAdmin, IsCompanyOwner


class AdminCompanyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = AdminCompanySerializer
    queryset = Company.objects.all()


class BookListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        user = request.user
        if user.role == 'admin' or user.role == 'viewer':
            books = Book.objects.all()
        elif Company.objects.filter(owner=user).exists():
            books = Book.objects.filter(company__owner__in=[user])
        elif user.role == 'author':
            books = Book.objects.filter(authors=user)
        elif user.role == 'publisher':
            books = Book.objects.filter(publisher=user)
        else:
            books = Book.objects.none()

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class AddBookAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsCompanyOwner]
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def perform_create(self, serializer):
        company = Company.objects.get(owner=self.request.user)
        serializer.save(company=company)