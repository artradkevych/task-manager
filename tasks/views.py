from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from tasks.forms import TaskForm, WorkerCreationForm, TeamForm
from tasks.models import (
    Task,
    Team,
    Worker,
    Tag,
    TaskType,
    Project,
    Position,
)


@login_required
def index(request):
    """View function for the home page of the site."""

    tasks_count = Task.objects.count()
    projects_count = Project.objects.count()
    teams_count = Team.objects.count()
    workers_count = Worker.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    latest_tasks = Task.objects.filter(
        assignees=request.user,
        status__in=("TODO", "IN_PROGRESS")
    ).select_related(
        "project",
        "task_type"
    ).prefetch_related("assignees", "tags")[:6]
    completed_tasks = Task.objects.filter(
        assignees=request.user,
        status="DONE"
    ).select_related(
        "project",
        "task_type"
    ).prefetch_related("assignees", "tags")[:6]

    context = {
        "tasks_count": tasks_count,
        "projects_count": projects_count,
        "teams_count": teams_count,
        "workers_count": workers_count,
        "num_visits": num_visits + 1,
        "latest_tasks": latest_tasks,
        "completed_tasks": completed_tasks
    }

    return render(request, "tasks/index.html", context=context)


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    context_object_name = "tag_list"
    paginate_by = 30


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("tasks:tag-list")


class TagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("tasks:tag-list")


class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("tasks:tag-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    context_object_name = "task_type_list"
    template_name = "tasks/task_type_list.html"
    paginate_by = 30


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "tasks/task_type_form.html"
    success_url = reverse_lazy("tasks:task_type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "tasks/task_type_form.html"
    success_url = reverse_lazy("tasks:task_type-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    paginate_by = 6


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
    success_url = reverse_lazy("tasks:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy("tasks:task-detail", kwargs={"pk": self.object.pk})


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    context_object_name = "project_list"
    paginate_by = 6


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["available_tasks"] = Task.objects.exclude(
            project=self.object
        )

        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    fields = "__all__"
    success_url = reverse_lazy("tasks:project-list")


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy("tasks:project-detail", kwargs={"pk": self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("tasks:project-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    context_object_name = "position_list"
    paginate_by = 30


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("tasks:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("tasks:position-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    context_object_name = "worker_list"
    paginate_by = 6


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["active_tasks"] = Task.objects.filter(
            assignees=self.object,
            status__in=("TODO", "IN_PROGRESS")
        )
        context["completed_tasks"] = Task.objects.filter(
            assignees=self.object,
            status__in=("DONE", "IN_REVIEW")
        )
        context["teams"] = Team.objects.all()

        return context


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("tasks:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerCreationForm

    def get_success_url(self):
        return reverse_lazy("tasks:worker-detail", kwargs={"pk": self.object.pk})


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("tasks:worker-list")


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    context_object_name = "team_list"
    paginate_by = 6


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["projects"] = Project.objects.all()

        return context


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy("tasks:team-list")


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamForm

    def get_success_url(self):
        return reverse_lazy("tasks:team-detail", kwargs={"pk": self.object.pk})


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("tasks:team-list")


@login_required
def send_task_to_review(request: HttpRequest, pk: int):
    task = Task.objects.get(id=pk)
    if (
        request.user in task.assignees.all()
        and task.status not in ("DONE", "IN_REVIEW")
    ):
        task.status = "IN_REVIEW"
        task.save()
    return HttpResponseRedirect(
        reverse_lazy("tasks:task-detail", args=[pk])
    )


@login_required
def approve_task(request: HttpRequest, pk: int):
    task = Task.objects.get(id=pk)
    if (
        request.user.is_staff
        and task.status == "IN_REVIEW"
    ):
        task.status = "DONE"
        task.save()
    return HttpResponseRedirect(
        reverse_lazy("tasks:task-detail", args=[pk])
    )

@login_required
def add_task_to_project(request: HttpRequest, pk: int):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":
        task_id = request.POST.get("task_id")

        if task_id:
            task = get_object_or_404(Task, pk=task_id)
            task.project = project
            task.save()

    return redirect("tasks:project-detail", pk=pk)

@login_required
def remove_task_from_project(request, pk: int, task_id: int):
    task = get_object_or_404(Task, pk=task_id)

    unassigned_project = Project.objects.get(name="Unassigned")

    if unassigned_project:
        task.project = unassigned_project
        task.save()

    return redirect("tasks:project-detail", pk=pk)


@login_required
def add_assignee(request: HttpRequest, pk: int):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        user_id = request.POST.get("worker_id")

        if user_id:
            worker = get_object_or_404(Worker, pk=user_id)
            task.assignees.add(worker)

    return redirect("tasks:task-detail", pk=pk)


@login_required
def remove_assignee(request: HttpRequest, pk: int, user_id: int):
    task = get_object_or_404(Task, pk=pk)
    worker = get_object_or_404(Worker, pk=user_id)

    if request.user.is_staff:
        task.assignees.remove(worker)

    return redirect("tasks:task-detail", pk=pk)


@login_required
def team_remove_project(request: HttpRequest, pk: int, project_id: int):
    project = get_object_or_404(Project, pk=project_id)

    blank_team = Team.objects.get(name="Blank")

    if blank_team:
        project.team = blank_team
        project.save()

    return redirect("tasks:team-detail", pk=pk)


@login_required
def toggle_assign_to_team(request: HttpRequest, pk: int):
    worker = Worker.objects.get(id=request.user.id)
    if (
        Team.objects.get(id=pk) in worker.teams.all()
    ):
        worker.teams.remove(pk)
    else:
        worker.teams.add(pk)
    return HttpResponseRedirect(reverse_lazy("tasks:team-detail", args=[pk]))


@login_required
def add_project_to_team(request: HttpRequest, pk: int):
    team = get_object_or_404(Team, pk=pk)

    if request.method == "POST":
        project_id = request.POST.get("project_id")

        if project_id:
            project = get_object_or_404(Project, pk=project_id)
            project.team = team
            project.save()

    return redirect("tasks:team-detail", pk=pk)

@login_required
def remove_project_from_team(request, pk: int, task_id: int):
    project = get_object_or_404(Project, pk=task_id)

    blank_team = Team.objects.get(name="Blank")

    if blank_team:
        project.team = blank_team
        project.save()

    return redirect("tasks:team-detail", pk=pk)
