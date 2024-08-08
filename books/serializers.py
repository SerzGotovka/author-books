from rest_framework import serializers
from rest_framework.response import Response
from .models import Author, Book
from typing import List, Dict, Any, Optional
import uuid

class BookSerializer(serializers.ModelSerializer):
    """Сериализатор для книг"""
    authors = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Book
        fields: List[str] = ['id', 'title', 'authors']


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор для авторов"""
    books: BookSerializer = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields: List[str] = ['id', 'name', 'books']


class AuthorRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с одним автором"""
    books = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Book.objects.all()
    )

    class Meta:
        model = Author
        fields: List[str] = ['id', 'name', 'books']

    def create(self, validated_data: Dict[str, Any]) -> Author:
        """Метод для создания автора"""
        books_data: List[Book] = validated_data.pop('books')
        author: Author = Author.objects.create(**validated_data)
        author.books.set(books_data)
        return author

    def update(self, instance: Author, validated_data: Dict[str, Any]) -> Author:
        """Метод для обновления автора"""
        books_data: Optional[List[Book]] = validated_data.pop('books', None)
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        if books_data is not None:
            instance.books.set(books_data)

        return instance

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Метод проверки при создании, что у автора есть хотя бы одна книга"""
        if not data.get("books"):
            raise serializers.ValidationError("У автора должна быть хотя бы одна книга")
        return data



















# ###############
# class BookListSerializers(serializers.ModelSerializer):
#     """Сериализатор для книг"""
#
#     class Meta:
#         model = Book
#         fields: List[str] = ["id", "title"]
#
# class AuthorSerializers(serializers.ModelSerializer):
#     """Сериализатор для авторов"""
#     books = BookListSerializers(many=True, read_only=False)
#     class Meta:
#         model = Author
#         fields = ['id', 'name', 'books']
#
#
#     def create(self, validated_data):
#         books_data = validated_data.pop('books')
#         author = Author.objects.create(**validated_data)
#         for book_data in books_data:
#             book, created = Book.objects.get_or_create(**book_data)
#             author.books.add(book)
#         return author
#
#
#
#
#
#
# class BookSerializers(serializers.ModelSerializer):
#     authors = AuthorSerializers(many=True)
#
#     class Meta:
#         model = Book
#         fields = ['id', 'title', 'authors']
#

    # def create(self, validated_data):
    #     authors_data = validated_data.pop('authors')
    #     book = Book.objects.create(**validated_data)
    #     for author_data in authors_data:
    #         author, created = Author.objects.get_or_create(**author_data)
    #         book.authors.add(author)
    #     return book

    # def update(self, instance, validated_data):
    #

    #     # Удаляем книги, которые не были переданы в запросе
    #     for book in current_books:
    #         if book not in new_books:
    #             instance.books.remove(book)

    #     return instance






























# from rest_framework import serializers
# from .models import Book, Author
# from typing import Type, List, Dict, Any
# import uuid


# class BookSerializers(serializers.ModelSerializer):
#     """Сериализатор для создания и обновления книг"""

#     authors = serializers.PrimaryKeyRelatedField(
#         many=True, read_only=False, queryset=Author.objects.all()
#     )

#     class Meta:
#         model = Book
#         fields: List[str] = ["id", "title", "authors"]

#     
    
#     def update(self, instance: Book, validated_data: Dict[str, Any]) -> Book:
#         """Метод для обновления книг"""
#         authors_ids: List[uuid.UUID] = validated_data.pop("authors", [])
#         instance.title = validated_data.get("title", instance.title)
#         instance.save()
#         instance.authors.set(authors_ids)
#         return instance

#     






#     def update(self, instance: Author, validated_data: Dict[str, Any]) -> Author:
#         """Метод для обновления авторов"""
#         books_ids: List[uuid.UUID] = validated_data.pop("books", [])
#         instance.name = validated_data.get("name", instance.name)
#         instance.save()
#         instance.books.set(books_ids)
#         return instance
