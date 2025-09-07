
**CRUD_operations.md**
```markdown
# CRUD Operations

## Create
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book
# Expected output: <Book: 1984 by George Orwell (1949)>


#Retrieve

book = Book.objects.get(id=1)
book.title, book.author, book.publication_year
# Expected output: ('1984', 'George Orwell', 1949)

#Update

book.title = "Nineteen Eighty-Four"
book.save()
book.title
# Expected output: 'Nineteen Eighty-Four'

#Delete 

book.delete()
# Expected output: (1, {'bookshelf.Book': 1})

Book.objects.all()
# Expected output: <QuerySet []>
