from django.urls import path
from .views import list_books
from .views import LibraryDetailView

urlpatterns = [
    path("books/", views.list_books, name="list_books"),  # FBV
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),  # CBV
]
