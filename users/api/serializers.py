from rest_framework import serializers

from auths.models import User
from users.models import Book, Company


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class AdminCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'owner', ]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id',
                  'title',
                  'company',
                  'publish_time',
                  'authors',
                  'publisher'
                  ]

    def create(self, validated_data):
        # Automatically assign the company based on the user
        company = Company.objects.get(owner=self.context['request'].user)
        validated_data['company'] = company
        return super().create(validated_data)
