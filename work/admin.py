from django.contrib import admin

from work.models import Task, Project


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
