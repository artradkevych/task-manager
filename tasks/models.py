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


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


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
    assignee = models.ForeignKey(
        Worker,
        related_name="tasks",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    project = models.ForeignKey(
        "Project",
        related_name="tasks",
        on_delete=models.PROTECT
    )
    tags = models.ManyToManyField("Tag", related_name="tasks")

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return f"{self.name} - {self.project} [{self.status}]"


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    workers = models.ManyToManyField(Worker,related_name="teams")

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


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
        ordering = ["is_active", "-created_at"]

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=65, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
