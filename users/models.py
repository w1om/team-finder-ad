from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from .constants import MAX_LENGTH_ABOUT, MAX_LENGTH_PHONE


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        extra_fields.setdefault("username", email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    avatar = models.ImageField(upload_to="avatars/", blank=True, verbose_name="Аватар")
    phone = models.CharField(max_length=MAX_LENGTH_PHONE, verbose_name="Телефон")
    github_url = models.URLField(blank=True, default="", verbose_name="Ссылка на GitHub")
    about = models.TextField(max_length=MAX_LENGTH_ABOUT, blank=True, default="", verbose_name="О себе")

    favorites = models.ManyToManyField(
        "projects.Project", related_name="interested_users", blank=True, verbose_name="Избранные проекты"
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone"]

    class Meta:
        ordering = ["-date_joined"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"