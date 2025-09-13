from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView

# Registration view
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log in user immediately after registration
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Use Django’s built-in LoginView and LogoutView
class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'


"""from django.shortcuts import render
from .models import Book
from django.views.generic.detail import DetailView
from .models import Library

# Function-based view
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'"""
