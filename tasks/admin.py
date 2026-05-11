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
        "get_assignees",
        "project",
        "deadline",
        "updated_at"
    )
    search_fields = (
        "name",
        "description",
        "assignees__username",
    )
    list_filter = (
        "status",
        "priority",
        "project",
        "task_type",
        "assignees",
    )
    filter_horizontal = ("assignees",)
    date_hierarchy = "deadline"

    @admin.display(description="Assignees")
    def get_assignees(self, obj):
        return ", ".join([user.username for user in obj.assignees.all()])


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
