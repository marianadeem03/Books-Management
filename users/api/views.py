# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Author, Publisher, Book
from users.api.serializers import AuthorSerializer, PublisherSerializer, BookSerializer


# Author views are not specifically requested but included for completeness
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.book_author.exists():
            return Response(
                {"error": "Cannot delete author with associated books."},
                status=status.HTTP_409_CONFLICT
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.book_publisher.exists():
            return Response(
                {"error": "Cannot delete publisher with associated books."},
                status=status.HTTP_409_CONFLICT
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BooksByPublisherAPIView(APIView):
    @staticmethod
    def get(request, publisher_id):
        books = Book.objects.filter(publisher_id=publisher_id)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BooksByTitleAPIView(APIView):
    @staticmethod
    def get(request, title):
        try:
            books = Book.objects.filter(title=title)
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
