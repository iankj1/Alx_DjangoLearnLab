from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

# Set up router
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Original ListAPIView route
    path('books/', BookList.as_view(), name='book-list'),

    # Router-generated CRUD routes
    path('', include(router.urls)),
]
