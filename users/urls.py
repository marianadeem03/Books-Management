from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.api.views import AuthorViewSet, PublisherViewSet, BookViewSet, BooksByPublisherAPIView, BooksByTitleAPIView

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'publishers', PublisherViewSet)
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('book_by_publishers/<int:publisher_id>/', BooksByPublisherAPIView.as_view(), name='books-by-publisher'),
    path('book_by_title/<str:title>/', BooksByTitleAPIView.as_view(), name='books-by-title'),
]
