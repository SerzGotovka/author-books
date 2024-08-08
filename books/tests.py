from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Book
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .views import *


class AuthorModelTests(TestCase):

    def test_create_author_name_strip(self):
        """Проверка, что пробелы в начале и в конце имени автора удаляются при сохранении"""
        author = Author.objects.create(name="   Author Name   ")
        self.assertEqual(author.name, "Author Name")


class AuthorListCreateViewTests(APITestCase):
    def setUp(self):
        # Создание книг для теста
        self.book1 = Book.objects.create(title="Book 1")
        self.book2 = Book.objects.create(title="Book 2")

    def test_create_author(self):
        url = reverse("author-list-create")
        data = {
            "name": "Test Author",
            "books": [str(self.book1.id), str(self.book2.id)],  # Передаем UUID книг
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 1)
        author = Author.objects.get()
        self.assertEqual(author.name, "Test Author")
        self.assertEqual(author.books.count(), 2)

    def test_list_authors(self):
        Author.objects.create(name="Author 1")
        Author.objects.create(name="Author 2")
        url = reverse("author-list-create")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class AuthorRetrieveUpdateDestroyViewTests(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Author to be fetched")
        self.url = reverse("author-detail", args=[str(self.author.id)])

    def test_retrieve_author(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.author.name)

    def test_delete_author(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)


class AuthorFilterNameViewTests(APITestCase):
    def setUp(self):
        Author.objects.create(name="John Doe")
        Author.objects.create(name="Jane Doe")

    def test_filter_author_by_name(self):
        url = reverse("author-filter-name")
        response = self.client.get(url, {"name": "John Doe"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "John Doe")


class AuthorFilterCountBooksViewTests(APITestCase):
    def setUp(self):
        author1 = Author.objects.create(name="Author with books")
        author2 = Author.objects.create(name="Author without books")
        book = Book.objects.create(title="Test Book")
        book.authors.add(author1)


class AuthorDeleteAllViewTests(APITestCase):
    def setUp(self):
        Author.objects.create(name="Author 1")
        Author.objects.create(name="Author 2")

    def test_delete_all_authors(self):
        url = reverse("author-delete-all")
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)


class BookFilterCountBooksViewTests(APITestCase):
    def setUp(self):
        self.author1 = Author.objects.create(name="Author 1")
        self.author2 = Author.objects.create(name="Author 2")

        self.book1 = Book.objects.create(title="Book with single author")
        self.book2 = Book.objects.create(title="Book with multiple authors")

        self.book1.authors.add(self.author1)
        self.book2.authors.add(self.author1, self.author2)


class BookModelTests(TestCase):

    def test_create_book_title_strip(self):
        """Проверка, что пробелы в начале и в конце названия книги удаляются при сохранении"""
        book = Book.objects.create(title="   Book Title   ")
        self.assertEqual(book.title, "Book Title")


class BookListCreateViewTests(APITestCase):
    def test_create_book(self):
        url = reverse("book-list-create")
        data = {"title": "Test Book"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, "Test Book")

    def test_list_books(self):
        Book.objects.create(title="Book 1")
        Book.objects.create(title="Book 2")
        url = reverse("book-list-create")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class BookRetrieveUpdateDestroyViewTests(APITestCase):
    def setUp(self):
        self.book = Book.objects.create(title="Book to be fetched")
        self.url = reverse("book-detail", args=[str(self.book.id)])

    def test_retrieve_book(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book.title)

    def test_update_book(self):
        data = {"title": "Updated Book"}
        response = self.client.put(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")

    def test_delete_book(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)


class BookFilterNameViewTests(APITestCase):
    def setUp(self):
        Book.objects.create(title="Book 1")
        Book.objects.create(title="Book 2")

    def test_filter_book_by_name(self):
        url = reverse("book-filter-name")
        response = self.client.get(url, {"title": "Book 1"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Book 1")


class BookFilterCountBooksViewTests(APITestCase):
    def setUp(self):
        author = Author.objects.create(name="Author 1")
        book1 = Book.objects.create(title="Book with single author")
        book2 = Book.objects.create(title="Book with multiple authors")
        book1.authors.add(author)
        book2.authors.add(author)


class BookDeleteAllViewTests(APITestCase):
    def setUp(self):
        Book.objects.create(title="Book 1")
        Book.objects.create(title="Book 2")

    def test_delete_all_books(self):
        url = reverse("book-delete-all")
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
