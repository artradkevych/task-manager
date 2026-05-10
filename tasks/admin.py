from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tasks.models import (
    Position,
    Worker,
    TaskType,
    Task,
    Team,
    Project,
    Tag
)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "position",
                    )
                },
            ),
        )
    )
    list_filter = UserAdmin.list_filter + ("position",)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "status",
        "priority",
        "assignee",
        "project",
        "deadline",
        "updated_at"
    )
    search_fields = (
        "name",
        "description",
        "assignee__username",
        "assignee__email"
    )
    list_filter = (
        "status",
        "priority",
        "project",
        "task_type",
        "assignee",
    )
    date_hierarchy = "deadline"


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "workers_count"
    )
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "team",
        "is_active",
        "created_at"
    )
    search_fields = ("name",)
    list_filter = (
        "is_active",
        "team",
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
