from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.api.views import BookListAPIView, AdminCompanyViewSet, AddBookAPIView

router = DefaultRouter()
router.register(r'admin_api/companies', AdminCompanyViewSet, basename='admin_companies')

urlpatterns = [
    path('book/view/', BookListAPIView.as_view(), name='book_list'),
    path('book/add/', AddBookAPIView.as_view(), name='add_book')
]

urlpatterns += router.urls
