from rest_framework import serializers
from .models import Author, Book
from typing import List, Dict, Any, Optional
import uuid


class BookSerializer(serializers.ModelSerializer):
    """Сериализатор для книг"""

    authors = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), many=True, required=False
    )

    class Meta:
        model = Book
        fields: List[str] = ["id", "title", "authors"]


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор для авторов"""

    books: BookSerializer = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields: List[str] = ["id", "name", "books"]


class AuthorRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с одним автором"""

    books = serializers.PrimaryKeyRelatedField(many=True, queryset=Book.objects.all())

    class Meta:
        model = Author
        fields: List[str] = ["id", "name", "books"]

    def create(self, validated_data: Dict[str, Any]) -> Author:
        """Метод для создания автора"""
        books_data: List[Book] = validated_data.pop("books")
        author: Author = Author.objects.create(**validated_data)
        author.books.set(books_data)
        return author

    def update(self, instance: Author, validated_data: Dict[str, Any]) -> Author:
        """Метод для обновления автора"""
        books_data: Optional[List[Book]] = validated_data.pop("books", None)
        instance.name = validated_data.get("name", instance.name)
        instance.save()

        if books_data is not None:
            instance.books.set(books_data)

        return instance

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Метод проверки при создании, что у автора есть хотя бы одна книга"""
        if not data.get("books"):
            raise serializers.ValidationError("У автора должна быть хотя бы одна книга")
        return data
