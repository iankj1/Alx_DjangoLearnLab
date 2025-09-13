from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Book
from django.views.generic import DetailView
from .models import Book, Library


# Function-based view: List all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "list_books.html", {"books": books})


# Class-based view: Library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = "library_detail.html"
    context_object_name = "library"
