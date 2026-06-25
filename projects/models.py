from django.conf import settings
from django.db import models

from .constants import MAX_LENGTH_PROJECT_NAME, MAX_LENGTH_STATUS


class ProjectStatus(models.TextChoices):
    OPEN = "open", "Open"
    CLOSED = "closed", "Closed"


class Project(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_PROJECT_NAME, verbose_name="Название проекта")
    description = models.TextField(blank=True, default="", verbose_name="Описание")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        verbose_name="Владелец",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    github_url = models.URLField(blank=True, default="", verbose_name="Ссылка на GitHub")
    status = models.CharField(
        max_length=MAX_LENGTH_STATUS,
        choices=ProjectStatus.choices,
        default=ProjectStatus.OPEN,
        verbose_name="Статус",
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="participated_projects",
        blank=True,
        verbose_name="Участники",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.name