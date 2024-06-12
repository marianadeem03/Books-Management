from django.contrib import admin
from users.models import Author, Publisher, Book
# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    '''Admin View for Author'''

    list_display = ('name', 'created', 'modified', 'id')
    list_filter = ('created', 'modified')
    readonly_fields = ('created', 'modified')
    search_fields = ('name',)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    '''Admin View for Publisher'''

    list_display = ('name', 'created', 'modified', 'id')
    list_filter = ('created', 'modified')
    readonly_fields = ('created', 'modified')
    search_fields = ('name',)


    @admin.register(Book)
    class BookAdmin(admin.ModelAdmin):
        '''Admin View for Book'''
    
        list_display = ('title', 'author', 'publisher', 'publish_date')
        list_filter = ('created', 'modified', 'publish_date')
        readonly_fields = ('created', 'modified',)
        search_fields = ('title', 'author__name', 'publisher__name')
