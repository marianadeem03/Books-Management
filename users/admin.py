from django.contrib import admin
from users.models import (Book,
                          Company,
                          BookFeedback)


# Register your models here.

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Admin View for Company"""
    filter_horizontal = ("authors", "publishers")

    list_display = ('name', 'owner', 'created', 'id')
    list_filter = ('created', 'modified')
    readonly_fields = ('created', 'modified')
    search_fields = ('name', 'owner__username')


@admin.register(BookFeedback)
class BookFeedbackAdmin(admin.ModelAdmin):
    """Admin View for BookFeedback"""

    list_display = (
        'book',
        'user',
        'comment_time',
        'id'
    )
    list_filter = ('comment_time', 'rating')
    readonly_fields = ('created', 'modified')
    search_fields = ('book__title', 'user__username',)

    @admin.register(Book)
    class BookAdmin(admin.ModelAdmin):
        """Admin View for Book"""
        filter_horizontal = ("authors",)

        list_display = (
            'title',
            'publisher',
            'company',
            'total_reviews',
            'rating',
            'publish_time'
        )
        list_filter = ('created', 'publish_time', 'rating',)
        readonly_fields = ('created', 'modified',)
        search_fields = ('title', 'company__name', 'publisher__name')
