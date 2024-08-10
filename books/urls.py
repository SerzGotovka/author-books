from django.urls import path
from .views import (
    AuthorListCreateView,
    AuthorRetrieveUpdateDestroyView,
    BookListCreateView,
    BookRetrieveUpdateDestroyView,
    AuthorFilterName,
    AuthorFilterCountBooks,
    AuthorDeleteAllView,
    BookFilterName,
    BookFilterCountBooks,
    BookDeleteAllView,
)

urlpatterns: list[path] = [
    path("api/authors/", AuthorListCreateView.as_view(), name="author-list-create"),
    path(
        "api/authors/<uuid:pk>/",
        AuthorRetrieveUpdateDestroyView.as_view(),
        name="author-detail",
    ),
    path("api/books/", BookListCreateView.as_view(), name="book-list-create"),
    path(
        "api/books/<uuid:pk>/",
        BookRetrieveUpdateDestroyView.as_view(),
        name="book-detail",
    ),
    path("api/author-name/", AuthorFilterName.as_view(), name="author-filter-name"),
    path(
        "api/author-count/",
        AuthorFilterCountBooks.as_view(),
        name="author-filter-countbook",
    ),
    path(
        "api/authors/delete-all/",
        AuthorDeleteAllView.as_view(),
        name="author-delete-all",
    ),
    path("api/book-name/", BookFilterName.as_view(), name="book-filter-name"),
    path(
        "api/book-count/", BookFilterCountBooks.as_view(), name="book-filter-countbook"
    ),
    path("api/book/delete-all/", BookDeleteAllView.as_view(), name="book-delete-all"),
]
