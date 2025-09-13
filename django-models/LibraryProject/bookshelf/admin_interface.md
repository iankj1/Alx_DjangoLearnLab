# Django Admin Interface Setup for Book Model

## Step 1: Register the Book Model
In `bookshelf/admin.py`:

```python
from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")
    list_filter = ("publication_year", "author")
    search_fields = ("title", "author")
