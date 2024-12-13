from rest_framework.routers import DefaultRouter
from users.api.views import (
    BooksViewSet,
    AdminCompanyViewSet,
    BookFeedbackViewSet
)

router = DefaultRouter()
router.register(r'companies', AdminCompanyViewSet, basename='admin_companies')
router.register(r'books', BooksViewSet, basename='company_books')
router.register(r'book_feedbacks', BookFeedbackViewSet, basename='books_feedbacks')

urlpatterns = [
]

urlpatterns += router.urls
