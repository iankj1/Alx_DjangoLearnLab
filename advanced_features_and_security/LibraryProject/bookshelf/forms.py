from django import forms
from .models import Book


class ExampleForm(forms.ModelForm):
    """
    Example form to demonstrate secure form handling with CSRF tokens.
    """
    class Meta:
        model = Book
        fields = ["title", "author"]
