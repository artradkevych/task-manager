from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from catalog.models import Tag, TaskType
from work.views import BaseSearchListView


class TagListView(BaseSearchListView):
    model = Tag
    context_object_name = "tag_list"
    paginate_by = 30
    search_fields = ["name"]


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("catalog:tag-list")


class TagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("catalog:tag-list")


class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("catalog:tag-list")


class TaskTypeListView(BaseSearchListView):
    model = TaskType
    context_object_name = "task_type_list"
    template_name = "catalog/task_type_list.html"
    paginate_by = 30
    search_fields = ["name"]


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "catalog/task_type_form.html"
    success_url = reverse_lazy("catalog:task_type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "catalog/task_type_form.html"
    success_url = reverse_lazy("catalog:task_type-list")
