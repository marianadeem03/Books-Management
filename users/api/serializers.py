# serializers.py
from rest_framework import serializers
from users.models import Author, Publisher, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'created', 'modified']


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'created', 'modified']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publisher', 'publish_date', 'created', 'modified']
        read_only_fields = ['created', 'modified']
