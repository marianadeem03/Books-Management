from rest_framework import serializers
from users.models import (
    Book,
    Company,
    BookFeedback
)


class AdminCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id',
            'name',
            'owner',
        ]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'company',
            'authors',
            'publisher',
            'publish_time',
            'total_reviews',
            'rating',
        ]

        extra_kwargs = {
            'total_reviews': {'read_only': True},
            'rating': {'read_only': True},
        }

    @staticmethod
    def validate_authors(value):
        for author in value:
            if not author.role == 'author':
                raise serializers.ValidationError(
                    f"Selected user {author.id} not have the role of author."
                )
        return value

    @staticmethod
    def validate_publisher(value):
        if not value.role == 'publisher':
            raise serializers.ValidationError(
                "Selected user must have the role of publisher."
            )
        return value


class BookFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookFeedback
        fields = [
            'id',
            'comment',
            'parent_comment',
            'rating',
            'user',
            'book',
            'comment_time'
        ]

    @staticmethod
    def validate_rating(value):
        if value and (value < 1 or value > 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate(self, data):
        rating = data.get('rating')
        if rating:
            book = data.get('book')
            request = self.context.get('request')
            user = request.user

            query = BookFeedback.objects.filter(
                book=book, user=user, rating__gt=0
            ).exists()
            if query:
                raise serializers.ValidationError("You have already rated this book.")
        return data
