from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Book, Author
from .serializers import AuthorSerializer, BookSerializer, AuthorRetrieveSerializer
from typing import Type
from django.db.models.query import QuerySet
from django.db.models import Count
from typing import List, Any
from rest_framework import serializers
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Author"])
class AuthorListCreateView(generics.ListCreateAPIView):
    """Класс для создания автора и получения всех авторов"""

    queryset: QuerySet[Author] = Author.objects.all()

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        if self.request.method == "POST":
            return AuthorRetrieveSerializer
        return AuthorSerializer


@extend_schema(tags=["Author"])
class AuthorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Класс для получения одного автора, изменения и удаления"""

    queryset: QuerySet[Author] = Author.objects.all()
    serializer_class = AuthorRetrieveSerializer


@extend_schema(tags=["Author"])
class AuthorFilterName(generics.ListAPIView):
    """Класс для получения отфильтрованных авторов по имени"""

    queryset: QuerySet[Author] = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends: List[Type[DjangoFilterBackend]] = [DjangoFilterBackend]
    filterset_fields: List[str] = ["name"]


@extend_schema(tags=["Author"])
class AuthorFilterCountBooks(generics.ListAPIView):
    """Класс для получения отфильтрованных авторов, у которых >=2 книг"""

    queryset: QuerySet[Author] = Author.objects.annotate(
        num_books=Count("books")
    ).filter(num_books__gte=2)
    serializer_class = AuthorSerializer


@extend_schema(tags=["Author"])
class AuthorDeleteAllView(generics.GenericAPIView):
    """Класс для удаления всех авторов"""

    queryset: QuerySet[Author] = Author.objects.all()
    serializer_class = AuthorSerializer

    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            authors: QuerySet[Author] = self.get_queryset()
            authors.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(tags=["Books"])
class BookListCreateView(generics.ListCreateAPIView):
    """Класс для создания книги и получения всех книг"""

    queryset: QuerySet[Book] = Book.objects.all()
    serializer_class = BookSerializer


@extend_schema(tags=["Books"])
class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Класс для получения одной книги, изменения и удаления"""

    queryset: QuerySet[Book] = Book.objects.all()
    serializer_class = BookSerializer


@extend_schema(tags=["Books"])
class BookFilterName(generics.ListAPIView):
    """Класс для получения отфильтрованных книг по названию"""

    queryset: QuerySet[Book] = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends: List[Type[DjangoFilterBackend]] = [DjangoFilterBackend]
    filterset_fields: List[str] = ["title"]


@extend_schema(tags=["Books"])
class BookFilterCountBooks(generics.ListAPIView):
    """Класс для получения отфильтрованных книг, у которых <=2 авторов"""

    queryset: QuerySet[Book] = Book.objects.annotate(
        num_authors=Count("authors")
    ).filter(num_authors__lt=2)
    serializer_class = BookSerializer


@extend_schema(tags=["Books"])
class BookDeleteAllView(generics.GenericAPIView):
    """Класс для удаления всех книг"""

    queryset: QuerySet[Book] = Book.objects.all()
    serializer_class = BookSerializer

    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            books: QuerySet[Book] = self.get_queryset()
            books.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
