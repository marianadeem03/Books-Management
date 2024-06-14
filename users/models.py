from django.db import models
from model_utils.models import TimeStampedModel

from auths.models import User


class Company(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company_owner')
    authors = models.ManyToManyField(User, related_name='company_authors')
    publishers = models.ManyToManyField(User, related_name='company_publishers')

    class Meta:
        db_table = "Company"
        verbose_name_plural = "Companies"
        managed = True
        ordering = ["-created"]

    def __str__(self):
        return self.name


class Book(TimeStampedModel):
    title = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_publisher')
    authors = models.ManyToManyField(User, related_name='book_authors')
    total_reviews = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    publish_time = models.DateTimeField()

    class Meta:
        db_table = "Book"
        verbose_name_plural = "Books"
        managed = True
        ordering = ["created"]

    def __str__(self):
        return self.title


class BookFeedback(TimeStampedModel):
    comment = models.TextField(null=True, blank=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True,
                                       on_delete=models.CASCADE, related_name='replies')
    rating = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_user')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_review')
    comment_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Book Feedback"
        verbose_name_plural = "Book Feedbacks"
        managed = True
        ordering = ["-comment_time"]

    def save(self, *args, **kwargs):
        if not self.id:
            existing_feedback = BookFeedback.objects.filter(user=self.user, book=self.book, rating__isnull=True).exists()
            if not existing_feedback:
                if self.rating is not None:
                    # Update book total reviews and average rating
                    self.book.total_reviews += 1
                    new_total_rating = (self.book.rating * (
                            self.book.total_reviews - 1) + self.rating) / self.book.total_reviews
                    self.book.rating = new_total_rating
                    self.book.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} - {self.book}'