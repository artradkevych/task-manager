from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from core.views import BaseSearchListView
from work.forms import (
    TaskForm,
    TaskSearchForm,
    ProjectSearchForm,
)
from work.models import (
    Task,
    Project,
)
from users.models import Worker


class TaskListView(BaseSearchListView):
    model = Task
    context_object_name = "task_list"
    paginate_by = 6
    search_form_class = TaskSearchForm
    search_fields = ["name", "description", "tags__name"]


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["available_workers"] = Worker.objects.exclude(
            tasks=self.object
        )

        return context


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("work:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy("work:task-detail", kwargs={"pk": self.object.pk})


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("work:task-list")


class ProjectListView(BaseSearchListView):
    model = Project
    context_object_name = "project_list"
    paginate_by = 9
    search_form_class = ProjectSearchForm
    search_fields = ["name", "description", "tasks__name"]


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unassigned = get_object_or_404(Project, name="Unassigned")

        context["available_tasks"] = Task.objects.filter(
            project=unassigned
        )

        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    fields = "__all__"
    success_url = reverse_lazy("work:project-list")


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy(
            "work:project-detail",
            kwargs={"pk": self.object.pk}
        )


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("work:project-list")


class SendTaskToReview(LoginRequiredMixin, generic.View):
    def post(self, request: HttpRequest, pk: int):
        task = get_object_or_404(Task, id=pk)
        if (
                request.user in task.assignees.all()
                and task.status not in ("DONE", "IN_REVIEW")
        ):
            task.status = "IN_REVIEW"
            task.save()
        return redirect("work:task-detail", pk=pk)


class ApproveTask(LoginRequiredMixin, generic.View):
    def post(self, request: HttpRequest, pk: int):
        task = get_object_or_404(Task, id=pk)
        if (
            request.user.is_staff
            and task.status == "IN_REVIEW"
        ):
            task.status = "DONE"
            task.save()
        return redirect("work:task-detail", pk=pk)


class AddTaskToProject(LoginRequiredMixin, generic.View):
    def post(self, request: HttpRequest, pk: int):
        project = get_object_or_404(Project, pk=pk)
        task_id = request.POST.get("task_id")

        if task_id:
            task = get_object_or_404(Task, pk=task_id)
            task.project = project
            task.save()

        return redirect("work:project-detail", pk=pk)


class RemoveTaskFromProject(LoginRequiredMixin, generic.View):
    def post(self, request, pk: int, task_id: int):
        task = get_object_or_404(Task, pk=task_id)
        unassigned_project = get_object_or_404(Project, name="Unassigned")

        task.project = unassigned_project
        task.save()

        return redirect("work:project-detail", pk=pk)


class AddAssignee(LoginRequiredMixin, generic.View):
    def post(self, request: HttpRequest, pk: int):
        task = get_object_or_404(Task, pk=pk)
        user_id = request.POST.get("worker_id")

        if user_id:
            worker = get_object_or_404(Worker, pk=user_id)
            task.assignees.add(worker)

        return redirect("work:task-detail", pk=pk)


class RemoveAssignee(LoginRequiredMixin, generic.View):
    def post(self, request: HttpRequest, pk: int, user_id: int):
        task = get_object_or_404(Task, pk=pk)
        worker = get_object_or_404(Worker, pk=user_id)

        if request.user.is_staff:
            task.assignees.remove(worker)

        return redirect("work:task-detail", pk=pk)
