from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Book

class BookAPITests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = APIClient()
        self.client.login(username='testuser', password='password123')

        # Create initial test books
        self.book1 = Book.objects.create(title='Book One', author='Author A', publication_year=2020)
        self.book2 = Book.objects.create(title='Book Two', author='Author B', publication_year=2022)

        self.list_url = reverse('book-list')

    def test_create_book(self):
        """✅ Test creating a new book"""
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'publication_year': 2024
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.get(id=response.data['id']).title, 'New Book')

    def test_list_books(self):
        """✅ Test retrieving the list of books"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_book(self):
        """✅ Test updating a book"""
        url = reverse('book-update', args=[self.book1.id])
        data = {'title': 'Updated Title', 'author': 'Author A', 'publication_year': 2021}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')

    def test_delete_book(self):
        """✅ Test deleting a book"""
        url = reverse('book-delete', args=[self.book2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filter_books_by_author(self):
        """✅ Test filtering books by author"""
        response = self.client.get(f"{self.list_url}?author=Author A")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], 'Author A')

    def test_search_books_by_title(self):
        """✅ Test searching books by title"""
        response = self.client.get(f"{self.list_url}?search=Book Two")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Book Two')

    def test_order_books_by_publication_year(self):
        """✅ Test ordering books by publication year descending"""
        response = self.client.get(f"{self.list_url}?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data[0]['publication_year'], response.data[1]['publication_year'])

    def test_permissions_required(self):
        """✅ Test that authentication is required for POST"""
        client = APIClient()  # new unauthenticated client
        data = {'title': 'Unauthorized Book', 'author': 'Anon', 'publication_year': 2023}
        response = client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
