from django.urls import path

from catalog.views import (
    TagListView,
    TagUpdateView,
    TagDeleteView,
    TagCreateView,
    TaskTypeListView,
    TaskTypeUpdateView,
    TaskTypeCreateView
)

urlpatterns = [
    path(
        "tags/",
        TagListView.as_view(),
        name="tag-list",
    ),
    path(
        "tags/<int:pk>/update/",
        TagUpdateView.as_view(),
        name="tag-update",
    ),
    path(
        "tags/<int:pk>/delete/",
        TagDeleteView.as_view(),
        name="tag-delete",
    ),
    path(
        "tags/create/",
        TagCreateView.as_view(),
        name="tag-create",
    ),
    path(
        "tasktypes/",
        TaskTypeListView.as_view(),
        name="task_type-list",
    ),
    path(
        "tasktypes/<int:pk>/update/",
        TaskTypeUpdateView.as_view(),
        name="task_type-update",
    ),
    path(
        "tasktypes/create/",
        TaskTypeCreateView.as_view(),
        name="task_type-create",
    ),
]

app_name = "catalog"
