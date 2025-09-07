from django.contrib import admin
from .models import Book

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Columns visible in the list view
    list_display = ("title", "author", "publication_year")
    list_filter = ("publication_year", "author")
    search_fields = ("title", "author")
