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
    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        required=False
    )

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
                    f"Selected user {author.id} not have the role of 'author'."
                )
        return value

    @staticmethod
    def validate_publisher(value):
        if not value.role == 'publisher':
            raise serializers.ValidationError(
                "Selected user must have the role of 'publisher'."
            )
        return value

    def validate(self, data):
        validated_data = super().validate(data)
        publisher = validated_data.get('publisher')
        self.validate_publisher(publisher)
        authors = validated_data.get('authors', [])
        self.validate_authors(authors)
        return validated_data

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        # If user is admin, ensure company is provided
        if user.role == 'admin':
            if 'company' not in validated_data:
                raise serializers.ValidationError(
                    {"company": "This field is required for admin users."}
                )
        else:
            # Automatically assign the company based on the user
            company = Company.objects.get(owner=user)
            validated_data['company'] = company

        return super().create(validated_data)


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
        if value is not None and (value < 1 or value > 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate(self, data):
        rating = data.get('rating')
        if rating:
            book = data.get('book')
            query = BookFeedback.objects.filter(
                book=book, user=self.context['request'].user, rating__gt=0
            ).exists()
            if query:
                raise serializers.ValidationError("You have already rated this book.")

        return data

    def create(self, validated_data):
        feedback = BookFeedback.objects.create(**validated_data)
        return feedback
