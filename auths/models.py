from django.db import models
from django.contrib.auth.models import AbstractUser

from auths.managers import UserManager


class User(AbstractUser):
    Roles = (
        ('admin', 'admin'),
        ('author', 'author'),
        ('viewer', 'viewer'),
        ('publisher', 'publisher'),
    )

    username = models.CharField(unique=False, max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=Roles)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password", "username"]

    class Meta:
        db_table = "User"
        verbose_name_plural = "Users"
        managed = True
        ordering = ["date_joined"]

    def __str__(self):
        return self.email
