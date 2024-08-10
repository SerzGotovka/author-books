from django.db import models
import uuid
from typing import Any


class Author(models.Model):
    """Модель для автора"""

    id: uuid.UUID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="id",
    )
    name: str = models.CharField(
        max_length=255, unique=True, null=False, blank=False, verbose_name="Полное имя"
    )

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Метод для сохранеения без пробелов в начале и конце"""
        self.name = self.name.strip()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "authors"
        verbose_name: str = "Автор"
        verbose_name_plural: str = "Авторы"


class Book(models.Model):
    """Модель для книг"""

    id: uuid.UUID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="id",
    )
    title: str = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Название книги",
    )
    authors: models.ManyToManyField = models.ManyToManyField(
        Author, verbose_name="авторы", related_name="books"
    )

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Метод для сохранеения без пробелов в начале и конце"""
        self.title = self.title.strip()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    class Meta:
        db_table = "books"
        verbose_name: str = "Книга"
        verbose_name_plural: str = "Книги"
