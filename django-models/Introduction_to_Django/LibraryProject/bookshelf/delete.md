# Delete Operation

```python
from bookshelf.models import Book

# Create a book (if none exists yet)
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Delete the book
book.delete()

# Verify deletion
Book.objects.all()
