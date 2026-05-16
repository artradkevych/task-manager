from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        related_name="workers",
        on_delete=models.PROTECT
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.position})"


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    workers = models.ManyToManyField(Worker, related_name="teams")

    @property
    def workers_count(self) -> int:
        return self.workers.count()

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
