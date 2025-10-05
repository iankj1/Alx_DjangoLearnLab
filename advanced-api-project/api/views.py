from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# Create your views here.
"""
Generic Views for Book CRUD operations using Django REST Framework.

Each view class below leverages DRF's built-in generics to reduce boilerplate
while still allowing for customization and permission control.
"""

# 📘 List all books (READ - open to everyone)
class BookListView(generics.ListAPIView):
    """
    GET /api/books/
    Returns a list of all books in the database.
    Public endpoint (no authentication required).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# 📖 Retrieve single book by ID (READ - open to everyone)
class BookDetailView(generics.RetrieveAPIView):
    """
    GET /api/books/<id>/
    Returns details of a single book identified by its primary key.
    Public endpoint (no authentication required).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# ➕ Create a new book (CREATE - authenticated users only)
class BookCreateView(generics.CreateAPIView):
    """
    POST /api/books/create/
    Creates a new book instance. Only authenticated users can create books.
    Includes validation via BookSerializer.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Optional: add custom behavior here
        serializer.save()


# ✏️ Update a book (UPDATE - authenticated users only)
class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /api/books/<id>/update/
    Updates an existing book. Only authenticated users can update books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Custom update logic if needed
        serializer.save()


# ❌ Delete a book (DELETE - authenticated users only)
class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/books/<id>/delete/
    Deletes a book. Only authenticated users can delete books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
