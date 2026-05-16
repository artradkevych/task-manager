from django.contrib.auth.models import AbstractUser
from django.db import models

from catalog.models import TaskType, Tag
from users.models import Worker, Team, Position


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=25,
        choices=[
            ("TODO", "Todo"),
            ("IN_PROGRESS", "In progress"),
            ("IN_REVIEW", "In review"),
            ("DONE", "Done")
        ],
        default="TODO"
    )
    priority = models.CharField(
        max_length=20,
        choices=[
            ("URGENT", "Urgent"),
            ("HIGH", "High"),
            ("MEDIUM", "Medium"),
            ("LOW", "Low"),
            ("OPTIONAL", "Optional")
        ],
        default="MEDIUM"
    )
    task_type = models.ForeignKey(
        TaskType,
        related_name="tasks",
        on_delete=models.PROTECT
    )
    assignees = models.ManyToManyField(
        Worker,
        related_name="tasks",
        blank=True,
    )
    project = models.ForeignKey(
        "Project",
        related_name="tasks",
        on_delete=models.CASCADE
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="tasks",
        blank=True
    )

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return f"{self.name} - {self.project} [{self.status}]"


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    team = models.ForeignKey(
        Team,
        related_name="projects",
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = ["-is_active", "-created_at"]

    def __str__(self) -> str:
        return self.name
