from datetime import date

from django.db import models
from model_utils.models import TimeStampedModel


# Create your models here.

class Author(TimeStampedModel):
    class Meta:
        db_table = "Author"
        verbose_name_plural = "Authors"
        managed = True
        ordering = ["created"]

    name = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Publisher(TimeStampedModel):
    class Meta:
        db_table = "Publisher"
        verbose_name_plural = "Publishers"
        managed = True
        ordering = ["created"]

    name = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Book(TimeStampedModel):
    class Meta:
        db_table = "Book"
        verbose_name_plural = "Books"
        managed = True
        ordering = ["created"]

    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name='book_author')
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT, related_name='book_publisher')
    publish_date = models.DateField(default=date.today)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} by {self.author.name}'
