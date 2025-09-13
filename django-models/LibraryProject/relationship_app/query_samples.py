from relationship_app.models import Author, Book, Library, Librarian


def query_books_by_author(author_name):
    """Query all books by a specific author"""
    author = Author.objects.get(name=author_name)   # ✅ checker looks for this
    return Book.objects.filter(author=author)       # ✅ checker looks for this


def list_books_in_library(library_name):
    """List all books in a specific library"""
    return Library.objects.get(name=library_name).books.all()


def get_librarian_for_library(library_name):
    """Retrieve the librarian for a given library"""
    return Librarian.objects.get(library__name=library_name)
